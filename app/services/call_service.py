from sqlalchemy.orm import Session
from app.models.call import CallCase
from app.services.state_machine import CallFlowMachine
from app.services.decision_engine import next_action
from app.services.medical_coding import medical_coder
from app.clients.nlu import parse_text
from app.clients.sentiment import analyze_sentiment
from app.clients.llm import structure_disclosure
from app.clients.queues import publish_imu_review, publish_stp


def create_case(db: Session, proposal_id: str, customer_phone: str, language: str, metadata: dict) -> CallCase:
    case = CallCase(
        proposal_id=proposal_id,
        customer_phone=customer_phone,
        language=language,
        metadata_json=metadata,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

async def process_utterance(db: Session, case: CallCase, text: str) -> dict:
    fsm = CallFlowMachine(case.status)
    nlu = await parse_text(text)
    sentiment = await analyze_sentiment(text)
    action = next_action(nlu, sentiment)

    # Extract symptoms and generate medical codes
    symptoms = medical_coder.extract_symptoms(text)
    medical_codes = medical_coder.generate_codes(symptoms)
    complexity_assessment = medical_coder.assess_complexity(symptoms, sentiment)

    # Check if call should end
    should_end = medical_coder.should_end_call(text, nlu.get("intent", {}).get("name", ""), symptoms)

    # Extract family member information if symptoms present
    family_record = None
    if symptoms:
        family_record = medical_coder.create_family_medical_record(text)

    # Store medical information in case
    if not case.structured_intake:
        case.structured_intake = {}
    case.structured_intake.update({
        "symptoms": symptoms,
        "medical_codes": medical_codes,
        "complexity_assessment": complexity_assessment,
        "family_record": family_record
    })

    # Handle call ending
    if should_end:
        fsm.complete()
        publish_stp({
            "proposal_id": case.proposal_id, 
            "status": "BOT_COMPLETED_CALL_ENDED",
            "reason": "user_initiated_end"
        })
        case.status = fsm.state
        case.transcript = (case.transcript or "") + f"\n{text}"
        db.add(case)
        db.commit()
        db.refresh(case)
        
        return {
            "status": case.status, 
            "nlu": nlu, 
            "sentiment": sentiment, 
            "action": "call_ended",
            "medical_codes": medical_codes,
            "symptoms": symptoms,
            "complexity_assessment": complexity_assessment,
            "should_end_call": True,
            "family_record": family_record
        }

    if action == "consent_ok":
        case.consent_captured = True
        if case.status in {"CONNECTED", "CONSENT_PENDING"}:
            fsm.ask_consent() if case.status == "CONNECTED" else None
            fsm.consent_ok()
    elif action == "nil_disclosure":
        case.nil_disclosure = True
        fsm.nil_done()
        publish_stp({"proposal_id": case.proposal_id, "status": "BOT_COMPLETED_NIL_DISCLOSURE"})
        fsm.complete()
    elif action == "route_imu":
        structured = await structure_disclosure(text)
        case.structured_intake.update(structured)
        case.nil_disclosure = False
        
        # Check if medical consultation is needed
        if complexity_assessment["requires_consultation"]:
            fsm.escalate()
            publish_imu_review(
                {
                    "proposal_id": case.proposal_id,
                    "phone": case.customer_phone,
                    "transcript": text,
                    "structured_intake": case.structured_intake,
                    "requires_consultation": True,
                    "medical_codes": medical_codes,
                    "symptoms": symptoms
                }
            )
        else:
            # Simple case - can complete without consultation
            fsm.complete()
            publish_stp({
                "proposal_id": case.proposal_id, 
                "status": "BOT_COMPLETED_MEDICAL_CODING",
                "medical_codes": medical_codes,
                "symptoms": symptoms
            })
        fsm.complete()
    elif action == "reschedule":
        fsm.reschedule()
    elif action == "rnr":
        fsm.mark_rnr()
    else:
        fsm.escalate()
        publish_imu_review(
            {
                "proposal_id": case.proposal_id,
                "phone": case.customer_phone,
                "transcript": text,
                "structured_intake": case.structured_intake,
                "reason": "low_confidence_or_negative_sentiment",
            }
        )

    case.transcript = (case.transcript or "") + f"\n{text}"
    case.status = fsm.state
    db.add(case)
    db.commit()
    db.refresh(case)
    
    return {
        "status": case.status, 
        "nlu": nlu, 
        "sentiment": sentiment, 
        "action": action,
        "medical_codes": medical_codes,
        "symptoms": symptoms,
        "complexity_assessment": complexity_assessment,
        "family_record": family_record,
        "should_end_call": should_end
    }
