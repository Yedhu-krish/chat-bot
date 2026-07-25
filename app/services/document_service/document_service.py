from app.database.models import Document,DocumentChunk
from sqlalchemy import select

def create_document(db,filename:str,s3_key:str,user_id:int,file_type:str,file_size:int):
    doc = Document(filename=filename,s3_key=s3_key,user_id=user_id,file_type=file_type,file_size=file_size)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db,document_id:int):
    stmnt = select(Document).where(Document.id == document_id)
    result = db.execute(stmnt)
    doc = result.scalar_one_or_none()
    return doc

def create_document_chunk(db,document_id:int,content:str,embedding:list[float],chunk_number:int):
    chunk = DocumentChunk(document_id=document_id,content=content,embedding=embedding,chunk_number=chunk_number)
    db.add(chunk)
    return chunk