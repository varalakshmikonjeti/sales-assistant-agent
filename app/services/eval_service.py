import re
from typing import Dict


def evaluate_response(response: str, context: str = "") -> Dict:
    """
    Production-style self-evaluation module.

    Scores:
    - groundedness → how tied response is to catalog/context
    - relevance → how well it answers the query
    - confidence → overall reliability estimate
    - flagged → risk detection signal
    """

    response_lower = response.lower()
    context_lower = context.lower()

    # =========================
    # 1. GROUNDEDNESS
    # =========================
    groundedness = 0.72  # base score

    # Strong catalog signal (pricing + enterprise features)
    if re.search(r"\$|\d+\/mo|users|sso|audit|sla", response_lower):
        groundedness += 0.18

    # Context overlap scoring (improved stability)
    response_words = set(response_lower.split())
    context_words = set(context_lower.split())

    if context_words:
        overlap_ratio = len(response_words & context_words) / max(1, len(response_words))
        groundedness += min(0.1, overlap_ratio)

    groundedness = min(0.99, groundedness)

    # =========================
    # 2. RELEVANCE
    # =========================
    relevance = 0.75

    keywords = ["plan", "price", "pricing", "enterprise", "starter", "growth", "features"]
    if any(k in response_lower for k in keywords):
        relevance += 0.18

    # reward informative answers
    if 10 <= len(response.split()) <= 80:
        relevance += 0.05

    relevance = min(0.99, relevance)

    # =========================
    # 3. CONFIDENCE (COMPOSITE SIGNAL)
    # =========================
    confidence = (groundedness * 0.55) + (relevance * 0.45)

    # penalty for fallback / uncertainty
    if any(x in response_lower for x in ["couldn't find", "not sure", "no information"]):
        confidence -= 0.18

    confidence = max(0.0, min(0.99, confidence))

    # =========================
    # 4. FLAGGING SYSTEM (INTERVIEW CRITICAL)
    # =========================
    flagged = False
    reason = "OK"

    if confidence < 0.65:
        flagged = True
        reason = "Low confidence response"

    if groundedness < 0.6:
        flagged = True
        reason = "Weak grounding in catalog/context"

    if "hallucination" in response_lower:
        flagged = True
        reason = "Explicit hallucination signal detected"

    # =========================
    # 5. FINAL OUTPUT (STRICT FORMAT)
    # =========================
    return {
        "groundedness": round(groundedness, 3),
        "relevance": round(relevance, 3),
        "confidence": round(confidence, 3),
        "flagged": flagged,
        "reasoning": reason
    }