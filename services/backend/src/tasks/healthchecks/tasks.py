# Standard Library imports
import time

# Core FastAPI imports

# Third-party imports
from src.worker import celery

# App imports


"""

    Здесь пример celery таска.
    В tasks.py важно импортировать инициализированный объект celery из src.worker.py

"""


@celery.task(name="create_task")
def create_task():
    print("task is create")
    time.sleep(1)
    print("task is done")
    return True
