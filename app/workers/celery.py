import logging
import os
from celery import Celery


logger = logging.getLogger(__name__)

celery_app = Celery('my_app',
             broker=os.environ.get("BROKER_URL"),
             backend=os.environ.get("BROKER_URL"),
             include=['app.workers.tasks'])

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    worker_hijack_root_logger=False,
)
