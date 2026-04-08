import httpx
from app.core.config import settings

async def parse_text(text: str) -> dict:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(settings.nlu_url, json={"text": text})
        response.raise_for_status()
        return response.json()
