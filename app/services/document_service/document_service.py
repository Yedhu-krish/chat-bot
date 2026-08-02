from sqlalchemy import select

from app.database.models import Document, DocumentChunk,ConversationDocument


def create_document(db,filename:str,s3_key:str,user_id:int,file_type:str,file_size:int,conversation_id:int):
    doc = Document(filename=filename,s3_key=s3_key,user_id=user_id,file_type=file_type,file_size=file_size)
    db.add(doc)
    db.flush()
    link = ConversationDocument(conversation_id=conversation_id,document_id=doc.id)
    db.add(link)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db,document_id:int):
    stmnt = select(Document).where(Document.id == document_id)
    result = db.execute(stmnt)
    doc = result.scalar_one_or_none()
    return doc

def get_document_ids_from_conversation(db,conversation_id:int):
    stmnt = select(ConversationDocument.document_id).where(ConversationDocument.conversation_id == conversation_id)
    result = db.execute(stmnt)
    document_ids = result.scalars().all()
    return document_ids

def create_document_chunk(db,document_id:int,content:str,embedding:list[float],chunk_number:int):
    chunk = DocumentChunk(document_id=document_id,content=content,embedding=embedding,chunk_number=chunk_number)
    db.add(chunk)
    return chunk

def get_document_list(db,current_user):
    stmnt = select(Document).where(Document.user_id == current_user.id)
    result = db.execute(stmnt)
    files = result.scalars().all()
    return [
    {
        "id": file.id,
        "file_name": file.filename,
        "status": file.status
    }
    for file in files
    ]