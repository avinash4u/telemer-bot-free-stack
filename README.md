# TeleMER Hybrid Voice Bot - Free Stack Production Scaffold

This repository is a production-grade starter scaffold for a **hybrid voice bot** that automates:
- consent capture
- nil disclosure collection
- reminders / reschedules / RNR follow-up calls
- routing only disclosed / escalated cases to IMU doctor or human agent

It is designed for the TeleMER problem statement where manual scripted calling is increasing AHT and repeat calls.

## What is included

- FastAPI **orchestrator** with a call state machine
- FreeSWITCH **ESL event handler** integration
- 5 **microservice wrappers**: ASR, NLU, TTS, Sentiment, LLM
- FreeSWITCH dialplan and `mod_event_socket` config
- Rasa OSS NLU training data for English + Hindi
- PostgreSQL models, Redis event streams, MinIO file storage
- RabbitMQ-backed STP + IMU queue publishers
- Optional unofficial WhatsApp client adapter using `whatsapp-web.js`
- Docker Compose for local development
- Example `.env`
- Stepwise production hardening notes

## Important implementation note

This repo is a **working scaffold / starter architecture**, not a fully certified call-center deployment. You still need to:
- connect an actual SIP trunk/provider
- load real ASR/TTS models
- train / tune Rasa with real transcripts
- tune dialer limits, retry windows, consent/compliance prompts
- add IAM / secret management / observability / HA for production

## Free stack used

- **Telephony / IVR / dialer:** FreeSWITCH
- **ASR:** Vosk (offline streaming)
- **NLU:** Rasa OSS
- **TTS:** Piper
- **Sentiment / frustration detection:** Hugging Face Transformers pipeline
- **LLM:** Ollama (local model serving)
- **API / orchestration:** FastAPI
- **DB:** PostgreSQL
- **Cache / event stream:** Redis Streams
- **Object storage:** MinIO
- **Queues:** RabbitMQ
- **WhatsApp fallback / reminders (non-official):** whatsapp-web.js

## High-level flow

1. Fresh payment lands in `payments` feed.
2. Orchestrator schedules outbound call via FreeSWITCH.
3. FreeSWITCH bridges call and opens an outbound ESL socket to FastAPI worker.
4. Bot greeting + consent prompt played.
5. Audio is sent to ASR -> transcript -> NLU.
6. If **nil disclosure** and consent captured, case is auto-closed as `BOT_COMPLETED`.
7. If disclosure / ambiguity / frustration detected, route to `imu.doctor.review` queue with structured intake.
8. RNR / reschedule logic is managed by status-driven retry rules.
9. Optional WhatsApp reminder is sent based on configured journey status.

## Local run

```bash
cp .env.example .env
docker compose up --build
```

Key services:
- Orchestrator: `http://localhost:8000`
- ASR: `http://localhost:8010`
- NLU: `http://localhost:5005`
- TTS: `http://localhost:8020`
- Sentiment: `http://localhost:8030`
- LLM: `http://localhost:11434`
- MinIO console: `http://localhost:9001`
- RabbitMQ mgmt: `http://localhost:15672`

## Suggested next step

Start with **bot-only nil disclosure + consent** for the top 60% scripted cases. Keep doctor / agent review for disclosed, low-confidence, silent, angry, or compliance-sensitive calls.
