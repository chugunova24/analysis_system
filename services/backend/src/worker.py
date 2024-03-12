# Standard Library imports

# Core FastAPI imports

# Third-party imports
from celery import Celery

# App imports
from src.config import settings


"""

Инициализация celery worker

"""


PATH_TASKS = [
    "src.tasks.healthchecks.tasks",
    "src.tasks.data.tasks",
]


celery = Celery(__name__,
                include=PATH_TASKS)


celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.beat_schedule = settings.CELERY_RESULT_BACKEND

celery.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'all_devices_analysis',
        'schedule': 10.0,
        # 'args': (16, 16)
    },
}

celery.conf.timezone = 'UTC'
