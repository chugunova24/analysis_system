# Standard Library imports

# Core FastAPI imports

# Third-party imports
from celery import shared_task

# App imports
from src.data.queries.orm import InfoDeviceORM
from src.db.session import sync_session_maker


"""
    Celery-таски для модуля data.
    Здесь лежит реализация отложенных аналитических задач с таймером.

"""


@shared_task(name="all_devices_analysis")
def all_devices_analysis():

    with sync_session_maker() as db:

        statistic = InfoDeviceORM.sync_get_statistic_all_time_all_devices(db=db)

    if statistic:
        return statistic._asdict()
    return statistic
