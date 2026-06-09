from sqlalchemy.orm import Session
from app.db.models import Message


class SQLiteMemory:

    def save_message(self, db: Session, user_id: str, role: str, message: str):
        msg = Message(
            user_id=user_id,
            role=role,
            message=message
        )
        db.add(msg)
        db.commit()
        return msg

    def get_history(self, db: Session, user_id: str):
        return (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .all()
        )

    def delete_memory(self, db: Session, user_id: str):
        deleted = (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .delete()
        )
        db.commit()
        return deleted

    def get_last_plan(self, db: Session, user_id: str):

        messages = (
            db.query(Message)
            .filter(Message.user_id == user_id)
            .order_by(Message.id.desc())
            .all()
        )

        plans = ["starter", "growth", "enterprise"]

        for msg in messages:

            text = msg.message.lower()

            for plan in plans:
                if plan in text:
                    return plan

        return None