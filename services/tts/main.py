import base64
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="TTS Service")

class TTSRequest(BaseModel):
    text: str
    voice: str = "en_US-lessac-medium"

@app.post("/synthesize")
def synthesize(payload: TTSRequest):
    fake_wav = base64.b64encode(f"VOICE::{payload.voice}::{payload.text}".encode()).decode()
    return {"audio_b64": fake_wav, "voice": payload.voice, "engine": "piper"}
