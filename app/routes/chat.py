from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.chat import InputData,ConversationInput
from app.services import llm,chat_service
from fastapi.responses import StreamingResponse
from app.database.database import get_db
from app.services import conversation_service
from typing import Optional
from app.services.auth_dependency import get_current_user
from app.database.models import User
from app.services.message_service import get_conversation_messsages

router = APIRouter()


@router.post("/new-conversation")
def create_conversation(request: ConversationInput,db:Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    conversation = conversation_service.create_conversation(db,user_id=current_user.id,title=request.title)
    return conversation

@router.get("/all-user-conversations")
def get_all_conversations(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    conversations = conversation_service.get_all_user_conversations(db,user_id=current_user.id)
    return conversations

@router.get("/conversation/{conversation_id}")
def get_conversation(conversation_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    conversation = conversation_service.get_user_conversation(db=db,conversation_id=conversation_id,user_id=current_user.id)
    return conversation

@router.delete("/conversation/{conversation_id}")
def remove_conversation(conversation_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return conversation_service.delete_conversation(db,conversation_id=conversation_id,user_id=current_user.id)


@router.post("/chat")
def readchat(request: InputData,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return StreamingResponse(chat_service.chat(db=db,conversation_id=request.conversation_id,message=request.message,user_id=current_user.id),media_type="text/plain")

@router.get("/conversation/{conversation_id}/messages")
def get_messages(conversation_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    messages = get_conversation_messsages(db=db,conversation_id=conversation_id,user_id=current_user.id)
    return messages