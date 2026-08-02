from app.database.models import User,Conversation,Message
from sqlalchemy import select
from app.services.conversation_service import get_user_conversation
from fastapi import HTTPException

# def get_or_create_user(db,username:str):
#     stmnt = select(User).where(User.username == username)
#     result = db.execute(stmnt)
#     user = result.scalar_one_or_none()
#     if user is None:
#         user = User(username=username)
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return user
#     return user


# def get_or_create_conversation(db,user_id:str):
#     stmnt = select(Conversation).where(Conversation.user_id == user_id)
#     result = db.execute(stmnt)
#     conversation = result.scalars().first()
#     if conversation is None:
#         conversation = Conversation(user_id=user_id)
#         db.add(conversation)
#         db.commit()
#         db.refresh(conversation)
#         return conversation

#     return conversation

def save_message(db,conversation_id:int,role:str,content:str):
    message = Message(conversation_id=conversation_id,role=role,content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_history(db,conversation_id:int):
    stmnt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    result = db.execute(stmnt)
    messages = result.scalars().all()
    data = []
    for message in messages:
        data.append (
            {
                "role":message.role,
                "content":message.content
            }
        )
    return data

def get_conversation_messsages(db,conversation_id:int,user_id:int):
    if not get_user_conversation(db=db,conversation_id=conversation_id,user_id=user_id):
        raise HTTPException(status_code=404,detail="Conversation not found")
    messages = get_history(db=db,conversation_id=conversation_id)
    return messages