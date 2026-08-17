from dotenv import load_dotenv
import os

load_dotenv()

# --------------------
# AI
# --------------------

OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_CHAT_URL = os.getenv("OLLAMA_CHAT_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


# --------------------
# Database
# --------------------

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# --------------------
# Authentication
# --------------------

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))


# --------------------
# AWS
# --------------------

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


# --------------------
# Redis / Celery
# --------------------

REDIS_URL = os.getenv("REDIS_URL")