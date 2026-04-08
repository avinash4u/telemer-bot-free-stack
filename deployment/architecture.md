# Architecture

```text
Dialer/CRM -> Orchestrator -> FreeSWITCH -> Customer
                         |         |
                         |         +-> ESL events/media control
                         |
                         +-> ASR (Vosk)
                         +-> NLU (Rasa)
                         +-> TTS (Piper)
                         +-> Sentiment service
                         +-> LLM (Ollama)
                         +-> PostgreSQL
                         +-> Redis Streams
                         +-> MinIO
                         +-> RabbitMQ -> STP / IMU queues
                         +-> WhatsApp adapter (optional)
```
