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

    from src.data.schemas.response import AnalysisDataOneDeviceResponse as schema

    with sync_session_maker() as db:

        statistic = InfoDeviceORM.sync_get_statistic_all_time_all_devices(db=db)

        statistic = [schema.model_validate(row).model_dump() for row in statistic]

    return statistic
