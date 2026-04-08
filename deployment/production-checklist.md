# Production checklist

## Phase 1: Narrow automation scope
- Only automate consent + nil disclosure + scripted reminders.
- Escalate any disclosure, silence, low confidence, language switch, negative sentiment, or legal/compliance edge case.

## Phase 2: Telephony hardening
- Use a proper SIP trunk / SBC.
- Add CPS caps, max concurrent channel limits, CLI masking, recording controls.
- Run FreeSWITCH active-passive or N+1.

## Phase 3: Model hardening
- Train Rasa on historical TeleMER transcripts.
- Add Hindi + Hinglish examples.
- Replace sentiment stub with calibrated transformer model.
- Add ASR confidence aggregation and no-input / barge-in handling.

## Phase 4: Workflow hardening
- Add case locking to prevent duplicate dials.
- Enforce retry policy:
  - fresh payments: round-robin, same-day SLA
  - RNR: N retries across time bands
  - reschedule: exact callback slot
- Make status-driven reminder workflows idempotent.

## Phase 5: Platform hardening
- Kubernetes + HPA for stateless services.
- External PostgreSQL with backups.
- Redis HA / Sentinel if needed.
- MinIO distributed mode if storing recordings at scale.
- RabbitMQ quorum queues.
- Add OpenTelemetry + Prometheus + Grafana + Loki.

## Phase 6: Governance
- Audit trail for every prompt, transcript, intent, decision, escalation, and agent takeover.
- PII redaction for logs.
- Data retention rules for recordings / transcripts.
- Human review for policy / medical ambiguity.
