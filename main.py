from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import json

from app.db.database import engine
from app.db.models import Base
from app.db.dependencies import get_db
from app.memory.sqlite_memory import SQLiteMemory
from app.models.schemas import ChatRequest
from app.agents.agent import run_agent
from app.tools.eval_tool import get_user_evals


# Create DB tables
Base.metadata.create_all(bind=engine)

# Memory instance
memory = SQLiteMemory()

app = FastAPI(title="Persistent Sales Assistant")


@app.get("/")
def root():
    return {"message": "Sales Assistant API Running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Persistent Sales Assistant",
        "version": "0.1.0"
    }


@app.get("/catalog")
def get_catalog():
    with open("catalog.json", "r") as file:
        return json.load(file)


@app.post("/chat/{user_id}")
def chat(user_id: str, request: ChatRequest, db: Session = Depends(get_db)):

    # Save user message
    memory.save_message(
        db=db,
        user_id=user_id,
        role="user",
        message=request.message
    )

    # Run agent (tools + memory + eval)
    result = run_agent(user_id, request.message, db)

    # Save assistant response
    memory.save_message(
        db=db,
        user_id=user_id,
        role="assistant",
        message=result["response"]
    )

    return result


@app.get("/chat/{user_id}/history")
def get_history(user_id: str, db: Session = Depends(get_db)):

    messages = memory.get_history(db=db, user_id=user_id)

    return [
        {
            "role": msg.role,
            "message": msg.message
        }
        for msg in messages
    ]


@app.delete("/chat/{user_id}/memory")
def delete_memory(user_id: str, db: Session = Depends(get_db)):

    deleted_count = memory.delete_memory(db=db, user_id=user_id)

    return {
        "message": "memory deleted successfully",
        "user_id": user_id,
        "records_removed": deleted_count
    }



@app.get("/chat/{user_id}/evals")
def user_evals(user_id: str, db: Session = Depends(get_db)):
    return get_user_evals(db, user_id)