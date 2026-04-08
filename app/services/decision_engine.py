from typing import Any

LOW_CONFIDENCE_THRESHOLD = 0.65
NEGATIVE_SENTIMENT_THRESHOLD = 0.70


def next_action(nlu: dict[str, Any], sentiment: dict[str, Any]) -> str:
    intent = nlu.get("intent", {}).get("name", "unknown")
    confidence = float(nlu.get("intent", {}).get("confidence", 0.0))
    neg_score = float(sentiment.get("negative", 0.0))

    if confidence < LOW_CONFIDENCE_THRESHOLD or neg_score >= NEGATIVE_SENTIMENT_THRESHOLD:
        return "human_review"
    if intent == "give_consent":
        return "consent_ok"
    if intent == "nil_disclosure":
        return "nil_disclosure"
    if intent == "has_disclosure":
        return "route_imu"
    if intent == "reschedule_request":
        return "reschedule"
    if intent == "not_reachable":
        return "rnr"
    return "human_review"
