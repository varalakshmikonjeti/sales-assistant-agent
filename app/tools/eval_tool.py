from sqlalchemy.orm import Session
from app.db.models import Message


def get_user_evals(db: Session, user_id: str):
    """
    TOOL: Analyze user conversation quality signals
    (simulates production observability dashboard data)
    """

    messages = (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .all()
    )

    total = len(messages)

    user_msgs = [m for m in messages if m.role == "user"]
    assistant_msgs = [m for m in messages if m.role == "assistant"]

    # simulate "quality scoring"
    high_quality_responses = min(len(assistant_msgs), int(len(assistant_msgs) * 0.85))
    low_quality_responses = len(assistant_msgs) - high_quality_responses

    avg_confidence_sim = 0.82 if total > 0 else 0.0

    return {
        "user_id": user_id,
        "total_messages": total,
        "user_messages": len(user_msgs),
        "assistant_messages": len(assistant_msgs),
        "high_confidence_responses_pct": round((high_quality_responses / max(1, len(assistant_msgs))) * 100, 2),
        "low_confidence_responses_pct": round((low_quality_responses / max(1, len(assistant_msgs))) * 100, 2),
        "avg_confidence": avg_confidence_sim
    }