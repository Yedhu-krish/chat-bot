from fastapi.routing import APIRouter
from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.models import User
from app.services.auth_dependency import get_current_user
from fastapi import UploadFile,File,Form
from app.services.document_service.storage_service import upload_file,delete_file_from_s3
from app.services.document_service.document_service import create_document,get_document_list
from app.celery_app.tasks import process_document
from app.schemas.doc import ConversationDocumentResponse
from fastapi.exceptions import HTTPException
from app.services.conversation_service import get_user_conversation

doc_router = APIRouter()


@doc_router.post("/documents/upload")
def file_upload(conversation_id:int = Form(...),file:UploadFile=File(...),db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    s3_key = upload_file(file_stream=file.file,file_name=file.filename,user_id=current_user.id)
    conversation = get_user_conversation(db,conversation_id=conversation_id,user_id=current_user.id)
    if conversation is None:
        raise HTTPException(status_code=404,detail="Conversation not found.")
    try:
        document = create_document(db=db,filename=file.filename,s3_key=s3_key,user_id=current_user.id,file_type=file.content_type,file_size=file.size,conversation_id=conversation_id)
    except Exception:
        delete_file_from_s3(s3_key=s3_key)
        raise HTTPException(status_code=400,detail="Error occured while processing the document !")
    process_document.delay(document_id=document.id)
    return document

@doc_router.get("/documents/{conversation_id}",response_model=list[ConversationDocumentResponse])
def list_files(conversation_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_document_list(db=db,current_user=current_user,conversation_id=conversation_id)