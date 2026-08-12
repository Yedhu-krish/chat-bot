from pydantic import BaseModel
from datetime import datetime

class ConversationDocumentResponse(BaseModel):
    id : int
    file_name: str
    created_at :  datetime