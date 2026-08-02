from app.services.message_service import get_history,save_message
from app.services.llm import get_ai_response
from app.services.prompts import SYSTEM_PROMPT
from app.services.conversation_service import get_user_conversation
from app.services.document_service.rag_service import question_handling
from app.services.document_service.document_service import get_document_ids_from_conversation
from fastapi.exceptions import HTTPException

# def chat(user_id:str,message:str):
#     add_message(user_id,"user",message)
#     history = get_history(user_id)
#     messages = [{
#         "role":"system",
#         "content":SYSTEM_PROMPT
#     }]
#     messages.extend(history)
#     # print(messages)
#     response_stream = get_ai_response(messages)
#     full_response = ""
#     for chunk in response_stream:
#         print(chunk)
#         full_response+=chunk
#         yield chunk
#     # response = get_ai_response(messages)
#     add_message(user_id,"assistant",full_response)


# def chat(db,username:str,message:str):
#     user = get_or_create_user(db,username=username)
#     conversation = get_or_create_conversation(db,user_id=user.id)
#     save_message(db,conversation_id=conversation.id,role="user",content=message)
#     history = get_history(db,conversation_id=conversation.id)
#     messages = [{
#         "role":"system",
#         "content":SYSTEM_PROMPT
#     }]
#     messages.extend(history)
#     response_stream = get_ai_response(messages)
#     full_response = ""
#     for chunk in response_stream:
#         # print(chunk)
#         full_response+=chunk
#         yield chunk
#     save_message(db,conversation_id=conversation.id,role="assistant",content=full_response)


def chat(db,conversation_id:int,message:str,user_id:int):
    # user = get_or_create_user(db,username=username)
    # conversation = get_or_create_conversation(db,user_id=user.id)
    conversation = get_user_conversation(db,conversation_id=conversation_id,user_id=user_id)
    if conversation is None:
        yield "Conversation Not Found"
        return
    document_ids = get_document_ids_from_conversation(db=db,conversation_id=conversation_id)
    if not document_ids:
        raise HTTPException(status_code=400,detail="No documents attached to this conversation.")
    print("DOCUMENT IDS OF THIS COVO ARE:",document_ids)
    save_message(db,conversation_id=conversation.id,role="user",content=message)
    history = get_history(db,conversation_id=conversation.id)
    messages = [{
        "role":"system",
        "content":SYSTEM_PROMPT
    }]
    messages.extend(history)
    context = question_handling(db=db,question=message,conversation_id=conversation_id)
    messages.extend(context)
    response_stream = get_ai_response(messages)
    full_response = ""
    for chunk in response_stream:
        # print(chunk)
        full_response+=chunk
        yield chunk
    save_message(db,conversation_id=conversation.id,role="assistant",content=full_response)