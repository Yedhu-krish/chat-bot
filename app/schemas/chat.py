from pydantic import BaseModel


class InputData(BaseModel):
    # username:str
    message:str
    conversation_id:int
    # user_id :str

class ConversationInput(BaseModel):
    user_id:int
    title:str
