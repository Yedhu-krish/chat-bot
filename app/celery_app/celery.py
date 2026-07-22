from celery import Celery
from app.config import REDIS_URL

celery_app = Celery("chatbot",broker=REDIS_URL,backend=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

celery_app.autodiscover_tasks(["app.celery_app"])