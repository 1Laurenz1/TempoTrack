from celery import Celery

from src.infrastructure.config.config_reader import settings


celery_app = Celery(
    "tempotrack",
    broker=settings.REDIS_URL.get_secret_value(),
    backend=settings.REDIS_URL.get_secret_value(),
)


celery_app.autodiscover_tasks(
    ['src.infrastructure.celery']
)