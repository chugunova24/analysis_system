# Standard Library imports
from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

import sqlalchemy.orm
# Core FastAPI imports

# Third-party imports
from sqlalchemy import select, text, and_
from sqlalchemy.sql import functions as func
import sqlalchemy

# App imports
from src.data.schemas import request as schema_request
from src.data.schemas import response as schema_response
from src.data.models import InfoDevice, Device


"""

    ORM-запросы для модуля data.

"""


stmt_median_x = func.percentile_cont(0.5).within_group(InfoDevice.x).label('mediana_x')
stmt_median_y = func.percentile_cont(0.5).within_group(InfoDevice.y).label('mediana_y')
stmt_median_z = func.percentile_cont(0.5).within_group(InfoDevice.z).label('mediana_z')

stmt_min_x = func.min(InfoDevice.x).label('min_x')
stmt_max_x = func.max(InfoDevice.x).label('max_x')
stmt_sum_x = func.sum(InfoDevice.x).label('sum_x')

stmt_min_y = func.min(InfoDevice.y).label('min_y')
stmt_max_y = func.max(InfoDevice.y).label('max_y')
stmt_sum_y = func.sum(InfoDevice.y).label('sum_y')

stmt_min_z = func.min(InfoDevice.z).label('min_z')
stmt_max_z = func.max(InfoDevice.z).label('max_z')
stmt_sum_z = func.sum(InfoDevice.z).label('sum_z')

stmt_count = func.count()


# Запросы к таблице InfoDevice (там хранятся данные, присылаемые устройствами)
class InfoDeviceORM:

    # Добавление одной ТЕСТОВОЙ записи в БД
    @staticmethod
    async def create_TEST_data(db: AsyncGenerator,
                               data: schema_request.TEST_InfoSchemaRequest):
        new_row = InfoDevice(**data.model_dump())

        db.add(new_row)
        await db.commit()
        await db.refresh(new_row)

        return new_row

    # Возвращает статистику за все время, сгруппированой по каждому устройству (общая статистика)
    @staticmethod
    def sync_get_statistic_all_time_all_devices(db: sqlalchemy.orm.session.Session):
        inner_stmt = [stmt_min_x, stmt_max_x, stmt_sum_x,
                      stmt_min_y, stmt_max_y, stmt_sum_y,
                      stmt_min_z, stmt_max_z, stmt_sum_z,
                      stmt_median_x, stmt_median_y, stmt_median_z,
                      stmt_count]

        # stmt = select(InfoDevice.device_id, *inner_stmt) \
        #     .group_by(InfoDevice.device_id)
        stmt = select(*inner_stmt)

        result = db.execute(stmt)

        # return result.all()
        return result.first()

    # Возвращает статистику по конкретному устройству.
    @staticmethod
    async def get_statistic_one_devices(db: AsyncGenerator,
                                        from_datetime: datetime,
                                        to_datetime: datetime,
                                        device_id: UUID):

        time = InfoDevice.created_at

        stmt_median_x_period = select(func.percentile_cont(0.5)
                                      .within_group(InfoDevice.x))
        stmt_median_y_period = select(func.percentile_cont(0.5)
                                      .within_group(InfoDevice.y))
        stmt_median_z_period = select(func.percentile_cont(0.5)
                                      .within_group(InfoDevice.z))

        # Если конец периода не указан, то устанавливается текущее время.
        # Если начало периода указано, то запрос будет учитывать период,
        # иначе будет вычислена статистика за все время относительно конкретного
        # устройства.
        if to_datetime is None:
            to_datetime = datetime.now()

        if from_datetime is not None:
            stmt_median_x_period = stmt_median_x_period \
                .where(time.between(from_datetime, to_datetime)) \
                .label('mediana_x')
            stmt_median_y_period = stmt_median_y_period \
                .where(time.between(from_datetime, to_datetime)) \
                .label('mediana_y')
            stmt_median_z_period = stmt_median_z_period \
                .where(time.between(from_datetime, to_datetime)) \
                .label('mediana_z')
        else:
            stmt_median_x_period = stmt_median_x_period.label('mediana_x')
            stmt_median_y_period = stmt_median_y_period.label('mediana_y')
            stmt_median_z_period = stmt_median_z_period.label('mediana_z')

        inner_stmt = [stmt_min_x, stmt_max_x, stmt_sum_x,
                      stmt_min_y, stmt_max_y, stmt_sum_y,
                      stmt_min_z, stmt_max_z, stmt_sum_z,
                      stmt_median_x_period,
                      stmt_median_y_period,
                      stmt_median_z_period,
                      stmt_count]

        stmt = select(InfoDevice.device_id, *inner_stmt) \
            .group_by(InfoDevice.device_id)

        if from_datetime and to_datetime:
            stmt = stmt.where(and_(time.between(from_datetime, to_datetime),
                                   InfoDevice.device_id == device_id))
        else:
            stmt = stmt.where(InfoDevice.device_id == device_id)

        result = await db.execute(stmt)
        result = result.first()

        return result


# Запросы к таблице Device (там хранятся uuid устройств)
class DeviceORM:

    # Добавление сгенерированного устройства в таблицу Device
    @staticmethod
    async def generate_device(db: AsyncGenerator):
        new_device = Device()

        db.add(new_device)
        await db.commit()
        await db.refresh(new_device)

        return schema_response.DeviceSchemaBase.model_validate(dict(device_id=new_device.id))


# Вывод результатов celery-таска
class TaskResultORM:

    @staticmethod
    async def get_celery_result(db: AsyncGenerator):
        stmt = """SELECT id, result FROM celery_taskmeta WHERE status='SUCCESS' ORDER BY date_done DESC LIMIT 1"""

        last_info = await db.execute(text(stmt))

        return last_info.first()
