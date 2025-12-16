from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.db import get_session
from .models import ChatMessage, ChatMessagePayload, ChatMessageListItem
router = APIRouter()

# /api/chat/
@router.get("/")
def chat_health():
    return {"status": "ok"}

# /api/chats/recent/
# curl http://localhost:8070/api/chats/recent/
@router.get("/recent/", response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results


# curl -X POST -d '{"message": "Hello world"}' -H "Content-Type: application/json" http://localhost:8070/api/chats/
#HTTP POST -> payload = {...}
@router.post("/", response_model=ChatMessage)
def chat_create_message(
    payload:ChatMessagePayload,
    session: Session = Depends(get_session)
):
    data = payload.model_dump()
    # create ChatMessage instance, persist it and return the saved object
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj