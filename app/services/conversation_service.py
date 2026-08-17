from app.database.models import Conversation,ConversationDocument
from sqlalchemy import select,delete
from sqlalchemy import func
from app.services.document_service.storage_service import delete_file_from_s3
from fastapi import HTTPException

def create_conversation(db,user_id:int,title:str=None):
    conversation = Conversation(user_id=user_id,title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_all_user_conversations(db,user_id:int):
    stmnt = (select(
        Conversation.id,
        Conversation.title,
        Conversation.created_at,
        func.count(ConversationDocument.id).label("doc_count")).outerjoin(ConversationDocument).where(Conversation.user_id == user_id).group_by(
            Conversation.id,
            Conversation.title,
            Conversation.created_at).order_by(Conversation.created_at))
    result = db.execute(stmnt)
    return [
        {
            "id": row.id,
            "title":row.title,
            "doc_count":row.doc_count,
            "created_at":row.created_at
        }
        for row in result
    ]

def get_user_conversation(db,conversation_id:int,user_id:int):
    stmnt = select(Conversation).where(Conversation.id == conversation_id,Conversation.user_id == user_id)
    result = db.execute(stmnt)
    conversation = result.scalar_one_or_none()
    return conversation

def delete_conversation(db,conversation_id:int,user_id:int):
    stmnt = select(Conversation).where(Conversation.id == conversation_id,Conversation.user_id == user_id)    
    conversation = db.execute(stmnt).scalar_one_or_none()
    if not conversation:
        return None
    stmnt2 = select(ConversationDocument).where(ConversationDocument.conversation_id == conversation_id)
    links = db.execute(stmnt2).scalars().all()
    s3_keys = [link.document.s3_key for link in links]
    for link in links:
        db.delete(link.document)
    db.delete(conversation)
    db.commit()
    for key in s3_keys:
        try:
            delete_file_from_s3(key)
        except Exception as e:
            raise HTTPException(status_code=500,detail=f"File deletion from s3 failed with error {e}")
    return{
        "message":"Conversation Deleted Successfully."
    }

