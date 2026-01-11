from celery.schedules import crontab

from .app import celery_app


celery_app.conf.beat_schedule = {
    "generate-daily-notifications": {
        "task": "tasks.generate_daily_notifications",
        "schedule": crontab(hour=0, minute=0)
    }
}