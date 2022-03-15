import os
from celery import Celery

broker = os.environ.get("CELERY_BROKER_URL", "redis://0.0.0.0:6379/0")
backend = os.environ.get("CELERY_BROKER_URL", "redis://0.0.0.0:6379/0")
app = Celery("tasks", broker=broker, backend=backend)
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "add-every-day": {
        "task": "tasks.tasks.predict_rate",
        "schedule": 5.0,
    },
}
