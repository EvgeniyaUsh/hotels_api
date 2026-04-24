from celery import Celery

from src.config import settings

celery_inst = Celery(
    "app", broker=settings.REDIS_URL, include=["src.tasks.tasks"]
)


celery_inst.conf.beat_schedule = {
    "send_emails": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
