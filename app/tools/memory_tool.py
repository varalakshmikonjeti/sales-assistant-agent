from sqlalchemy.orm import Session
from app.db.models import Message


def get_user_memory(db: Session, user_id: str, limit: int = 10):
    """
    TOOL: Fetch user memory (required by assignment)
    """
    messages = (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(Message.id.desc())
        .limit(limit)
        .all()
    )

    # reverse to maintain chronological order
    messages = list(reversed(messages))

    return [
        {
            "role": m.role,
            "message": m.message
        }
        for m in messages
    ]


def save_memory(db: Session, user_id: str, role: str, message: str):
    """
    TOOL: Save message
    """
    msg = Message(
        user_id=user_id,
        role=role,
        message=message
    )
    db.add(msg)
    db.commit()
    return msg


def delete_memory(db: Session, user_id: str):
    """
    TOOL: HARD DELETE (GDPR RESET)
    """
    deleted = (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .delete()
    )
    db.commit()

    return deleted