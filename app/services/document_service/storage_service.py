from app.services.document_service.client import client
from uuid import uuid4
from pathlib import Path
from app.config import S3_BUCKET_NAME

def generate_s3_key(file_name:str,user_id:int) -> str:
    name = Path(file_name).name.lower()
    return f"documents/{user_id}/{uuid4()}-{name}"


def upload_file(file_stream,user_id:int,file_name:str) ->str:
    s3_key = generate_s3_key(file_name=file_name,user_id=user_id)
    client.upload_fileobj(Fileobj=file_stream,Bucket=S3_BUCKET_NAME,Key=s3_key)
    return s3_key

def download_file_from_s3(s3_key:str) ->bytes:
    response = client.get_object(Bucket=S3_BUCKET_NAME,Key=s3_key)
    with response["Body"] as stream:
        return stream.read()
    
def delete_file_from_s3(s3_key:str):
    response = client.delete_object(Bucket=S3_BUCKET_NAME,Key=s3_key)
    return response