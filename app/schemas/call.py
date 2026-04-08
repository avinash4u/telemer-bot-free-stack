from datetime import datetime
from pydantic import BaseModel, Field

class CreateCallCase(BaseModel):
    proposal_id: str = Field(..., examples=["PROP-123"])
    customer_phone: str
    language: str = "en"
    metadata: dict = {}

class CallCaseResponse(BaseModel):
    id: int
    proposal_id: str
    customer_phone: str
    language: str
    status: str
    created_at: datetime

class InboundUtterance(BaseModel):
    session_id: str
    text: str
    confidence: float = 1.0
    metadata: dict = {}
