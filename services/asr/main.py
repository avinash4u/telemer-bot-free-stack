from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ASR Service")

class ASRRequest(BaseModel):
    audio_b64: str
    language: str = "en"

@app.post("/transcribe")
def transcribe(payload: ASRRequest):
    # Replace with actual Vosk streaming / batch decoding.
    return {"text": "", "confidence": 0.0, "language": payload.language, "engine": "vosk"}
