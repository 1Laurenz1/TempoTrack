from celery import Celery
from celery.schedules import schedule

from src.infrastructure.config.config_reader import settings


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


celery_app.conf.beat_schedule.update({
    "check-notifications-every-10-seconds": {
        "task": "tasks.generate_schedule_notifications",
        "schedule": schedule(10.0),
    },
})


celery_app.autodiscover_tasks(
    ['src.infrastructure.celery.tasks']
)



import src.infrastructure.celery.tasks.generate_schedule_notifications
import src.infrastructure.celery.tasks.send_schedule_notification