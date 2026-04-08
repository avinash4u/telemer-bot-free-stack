from app.clients.http import JsonHttpClient
from app.core.config import settings

client = JsonHttpClient(settings.sentiment_url)

async def analyze_sentiment(text: str) -> dict:
    return await client.post("/analyze", {"text": text})
