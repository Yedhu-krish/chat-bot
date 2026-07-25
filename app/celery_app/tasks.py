from app.celery_app.celery import celery_app
from app.services.document_service.document_service import get_document,create_document_chunk
from app.database.models import DocumentStatus
from app.database.database import SessionLocal
from app.services.document_service.storage_service import download_file_from_s3
from app.services.document_service.pdf_service import extract_text_from_pdf
from app.services.document_service.chunk_service import chunk_text
from app.services.document_service.embedding_service import generate_embedding

@celery_app.task
def msg():
    print( "Hello world")


@celery_app.task
def process_document(document_id:int):
    db = SessionLocal()
    doc = None
    try:
        doc = get_document(db=db,document_id=document_id)
        pdf_bytes = download_file_from_s3(s3_key=doc.s3_key)
        text = extract_text_from_pdf(pdf_bytes=pdf_bytes)
        chunks = chunk_text(text=text)
        for index,chunk in enumerate(chunks):
            embedding = generate_embedding(chunk=chunk)
            create_document_chunk(db=db,document_id=doc.id,content=chunk,embedding=embedding,chunk_number=index)
            print("====chunking completed======")
        doc.status = DocumentStatus.READY
        db.commit()
    except Exception as e:
        if doc:
            doc.status = DocumentStatus.FAILED
            doc.error_message = str(e)
    finally:
        db.commit()
        db.close()
