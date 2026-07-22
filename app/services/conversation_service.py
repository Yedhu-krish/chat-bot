from app.database.models import Conversation
from sqlalchemy import select,delete


def create_conversation(db,user_id:int,title:str=None):
    conversation = Conversation(user_id=user_id,title=title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_all_user_conversations(db,user_id:int):
    stmnt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at)
    result = db.execute(stmnt)
    conversations = result.scalars().all()
    return [
        {
            "id": conversation.id,
            "title":conversation.title,
            "created_at":conversation.created_at
        }
        for conversation in conversations
    ]

def get_user_conversation(db,conversation_id:int,user_id:int):
    stmnt = select(Conversation).where(Conversation.id == conversation_id,Conversation.user_id == user_id)
    result = db.execute(stmnt)
    conversation = result.scalar_one_or_none()
    return conversation

def delete_conversation(db,conversation_id:int,user_id:int):
    stmnt = delete(Conversation).where(Conversation.id == conversation_id,Conversation.user_id==user_id)
    db.execute(stmnt)
    db.commit()
    return {
        "message": "Conversation Deleted Successfully."
    }








