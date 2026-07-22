from fastapi.routing import APIRouter
from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.models import User
from app.services.auth_dependency import get_current_user
from fastapi import UploadFile,File
from app.services.document_service.storage_service import upload_file,delete_file_from_s3
from app.services.document_service.document_service import create_document
from app.celery_app.tasks import process_document

doc_router = APIRouter()


@doc_router.post("/upload")
def file_upload(file:UploadFile=File(...),db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    s3_key = upload_file(file_stream=file.file,file_name=file.filename,user_id=current_user.id)
    try:
        document = create_document(db=db,filename=file.filename,s3_key=s3_key,user_id=current_user.id,file_type=file.content_type,file_size=file.size)
    except Exception:
        delete_file_from_s3(s3_key=s3_key)
    process_document.delay(document_id=document.id)
    return document