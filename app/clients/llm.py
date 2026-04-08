import httpx
from app.core.config import settings

async def structure_disclosure(text: str) -> dict:
    prompt = (
        "Extract structured TeleMER medical disclosure JSON from the following patient statement. "
        "Return strict JSON with keys: symptoms, diagnoses, medications, hospitalization_history, risk_flags, summary.\n\n"
        f"Statement: {text}"
    )
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.llm_url}/api/generate",
                json={"model": settings.llm_model, "prompt": prompt, "stream": False},
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        # Fallback when LLM is not available
        return {
            "symptoms": [],
            "diagnoses": [],
            "medications": [],
            "hospitalization_history": [],
            "risk_flags": ["llm_unavailable"],
            "summary": text,
            "error": str(e)
        }
