from pydantic import BaseModel

class DocumentList(BaseModel):
    id : int
    file_name: str
    status :  str