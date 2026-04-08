from sqlalchemy.orm import Session
from app.models.call import CallCase
from app.services.state_machine import CallFlowMachine
from app.services.decision_engine import next_action
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
        case.structured_intake = structured
        case.nil_disclosure = False
        fsm.escalate()
        publish_imu_review(
            {
                "proposal_id": case.proposal_id,
                "phone": case.customer_phone,
                "transcript": text,
                "structured_intake": structured,
            }
        )
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
                "reason": "low_confidence_or_negative_sentiment",
            }
        )

    case.transcript = (case.transcript or "") + f"\n{text}"
    case.status = fsm.state
    db.add(case)
    db.commit()
    db.refresh(case)
    return {"status": case.status, "nlu": nlu, "sentiment": sentiment, "action": action}
