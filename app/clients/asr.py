from app.clients.http import JsonHttpClient
from app.core.config import settings

client = JsonHttpClient(settings.asr_url)

async def transcribe(audio_b64: str, language: str = "en") -> dict:
    return await client.post("/transcribe", {"audio_b64": audio_b64, "language": language})
