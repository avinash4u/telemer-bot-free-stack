import httpx

class JsonHttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def post(self, path: str, payload: dict):
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(f"{self.base_url}{path}", json=payload)
            response.raise_for_status()
            return response.json()
