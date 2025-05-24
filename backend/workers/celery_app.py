
# backend/workers/celery_app.py - Ensure this exists
from celery import Celery
import os

# Configure Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "voice_dubbing_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["workers.tasks.audio_tasks", "workers.tasks.ml_tasks", "workers.tasks.video_tasks"]
)

# Configure Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes max per task
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)