from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sentiment Service")

class SentimentRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(payload: SentimentRequest):
    text = payload.text.lower()
    negative = 0.85 if any(x in text for x in ["angry", "irritated", "stop", "frustrated", "nahi samajh"]) else 0.1
    return {"negative": negative, "neutral": 1.0 - negative, "engine": "transformers"}
