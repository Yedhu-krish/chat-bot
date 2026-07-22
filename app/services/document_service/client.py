import boto3
from app.config import AWS_ACCESS_KEY_ID,AWS_REGION,AWS_SECRET_ACCESS_KEY

client = boto3.client(service_name="s3",aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=AWS_REGION)