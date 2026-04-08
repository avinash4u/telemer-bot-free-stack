from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.db import get_db
from app.schemas.call import CreateCallCase, InboundUtterance
from app.services.call_service import create_case, process_utterance
from app.services.calling_service import calling_service
from app.models.call import CallCase
from pydantic import BaseModel

router = APIRouter()

class OutboundCallRequest(BaseModel):
    phone_number: str
    caller_id: str = "TeleMER"
    proposal_id: Optional[str] = None
    metadata: Optional[dict] = {}

@router.post("", status_code=201)
def create_call_case(payload: CreateCallCase, db: Session = Depends(get_db)):
    case = create_case(db, payload.proposal_id, payload.customer_phone, payload.language, payload.metadata)
    return {
        "id": case.id,
        "proposal_id": case.proposal_id,
        "customer_phone": case.customer_phone,
        "language": case.language,
        "status": case.status,
        "created_at": case.created_at,
    }

@router.post("/{case_id}/utterance")
async def handle_utterance(case_id: int, payload: InboundUtterance, db: Session = Depends(get_db)):
    case = db.get(CallCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    return await process_utterance(db, case, payload.text)

@router.get("/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.get(CallCase, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    return {
        "id": case.id,
        "proposal_id": case.proposal_id,
        "phone": case.customer_phone,
        "status": case.status,
        "consent_captured": case.consent_captured,
        "nil_disclosure": case.nil_disclosure,
        "structured_intake": case.structured_intake,
        "transcript": case.transcript,
    }

@router.post("/outbound")
async def make_outbound_call(payload: OutboundCallRequest, db: Session = Depends(get_db)):
    """Make outbound call to phone number"""
    try:
        # Create call case first
        case = create_case(
            db, 
            payload.proposal_id or f"OUTBOUND_{payload.phone_number}",
            payload.phone_number,
            "en",
            payload.metadata
        )
        
        # Initiate outbound call
        success = await calling_service.make_outbound_call(
            payload.phone_number,
            payload.caller_id
        )
        
        if success:
            return {
                "success": True,
                "call_id": case.id,
                "phone_number": payload.phone_number,
                "status": "initiated",
                "message": "Outbound call initiated successfully"
            }
        else:
            return {
                "success": False,
                "call_id": case.id,
                "phone_number": payload.phone_number,
                "status": "failed",
                "message": "Failed to initiate outbound call"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making outbound call: {str(e)}")

@router.post("/{call_id}/hangup")
async def hangup_call(call_id: int, db: Session = Depends(get_db)):
    """Hangup active call"""
    try:
        success = await calling_service.hangup_call(str(call_id))
        return {
            "success": success,
            "call_id": call_id,
            "message": "Call hangup initiated" if success else "Failed to hangup call"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error hanging up call: {str(e)}")
