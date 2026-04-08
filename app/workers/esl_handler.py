"""
Outbound ESL handler skeleton.

Expected FreeSWITCH dialplan usage:
  <action application="socket" data="orchestrator:8084 async full"/>

For production, replace this stub with a real ESL server using libesl or a maintained Python ESL binding.
Recommended responsibilities:
- receive CHANNEL_PARK / ANSWER / HANGUP events
- play prompts / collect DTMF
- bridge media with ASR/TTS services
- update orchestrator state via HTTP callbacks
"""

from fastapi import FastAPI

app = FastAPI(title="ESL Handler")

@app.get("/health")
def health():
    return {"ok": True, "service": "esl-handler"}
