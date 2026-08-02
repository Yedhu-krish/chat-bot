from pydantic import BaseModel


class InputData(BaseModel):
    message:str
    conversation_id:int
    # document_id:int

class ConversationInput(BaseModel):
    title:str
