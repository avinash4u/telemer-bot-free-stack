from app.clients.http import JsonHttpClient
from app.core.config import settings

client = JsonHttpClient(settings.tts_url)

async def synthesize(text: str, voice: str = "en_US-lessac-medium") -> dict:
    return await client.post("/synthesize", {"text": text, "voice": voice})
