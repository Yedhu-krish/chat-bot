from app.celery_app.celery import celery_app
from app.services.document_service.document_service import get_document 
from app.database.models import DocumentStatus
from app.database.database import SessionLocal
from app.services.document_service.storage_service import download_file_from_s3
from app.services.document_service.pdf_service import extract_text_from_pdf
from app.services.document_service.chunk_service import chunk_text

@celery_app.task
def msg():
    print( "Hello world")


@celery_app.task
def process_document(document_id:int):
    db = SessionLocal()
    try:
        doc = get_document(db=db,document_id=document_id)
        pdf_bytes = download_file_from_s3(s3_key=doc.s3_key)
        text = extract_text_from_pdf(pdf_bytes=pdf_bytes)
        print("====Extracted texts are=======")
        print(text[:500])
        chunks = chunk_text(text=text)
        print("+++++",len(chunks),"+++++++")
        print(chunks[0])
        print(chunks[1])
        doc.status = DocumentStatus.READY
        db.commit()
        db.refresh(doc)
    except Exception as e:
        doc.status = DocumentStatus.FAILED
        doc.error_message = str(e)
    finally:
        db.close()
