from celery import Celery

from src.infrastructure.config.config_reader import settings

from .beat import *

celery_app = Celery(
    "tempotrack",
    broker=settings.REDIS_URL.get_secret_value(),
    backend=settings.REDIS_URL.get_secret_value(),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_default_queue="default",
)


celery_app.autodiscover_tasks(
    ['src.infrastructure.celery']
)