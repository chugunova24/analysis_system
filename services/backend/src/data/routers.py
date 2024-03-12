# Standard Library imports
import asyncio
import pickle
from select import select
from typing import AsyncGenerator, Optional, Any
from datetime import datetime
from uuid import UUID

import sqlalchemy
# Core FastAPI imports
from fastapi import APIRouter, Depends, WebSocket, Request
from fastapi_restful.cbv import cbv

# Third-party imports
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.data.models import InfoDevice
from src.data.queries.init_data import bulk_new_devices, bulk_new_info_device
# App imports
from src.db.session import get_async_session, sync_session_maker
from src.main import templates
from src.data.queries.orm import InfoDeviceORM, DeviceORM, TaskResultORM
import src.data.schemas.response as schema_res
import src.data.schemas.request as schema_req


"""

    Обработка маршрутов модуля data.

"""

router = APIRouter()

datetime_format = '%Y-%m-%d %H:%M:%S'


# get_current_user = fastapi_users.current_user()

# db: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)


@cbv(router)
class DataView:
    db: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)


    @router.get("/realtime")
    async def get(self, request: Request):
        """
        Возвращает шаблон, который является реализацией клиентской стороны.
        В этот же шаблон подгружаются данные (общая статистика) каждые 15 секунд.
        """
        return templates.TemplateResponse(
            request=request, name="realtime.html", context={"id": id}
        )

    @router.post("/",
                 status_code=status.HTTP_201_CREATED,
                 response_model=schema_res.InfoSchemaResponse)
    async def create_row(self,
                         data: schema_req.InfoSchemaRequest) -> schema_res.InfoSchemaResponse:
        """
        Добавление одной записи, отправленной устройством, в БД
        """
        new_row = await InfoDeviceORM.create_data(db=self.db,
                                                  data=data)

        return new_row

    @router.post("/test_data",
                 status_code=status.HTTP_201_CREATED,
                 response_model=schema_res.InfoSchemaResponse)
    async def create_TEST_row(self,
                              data: schema_req.TEST_InfoSchemaRequest) -> schema_res.InfoSchemaResponse:
        """
        Добавление ТЕСТОВОЙ записи в базу данных
        """
        new_row = await InfoDeviceORM.create_TEST_data(db=self.db,
                                                       data=data)

        return new_row


@cbv(router)
class DeviceView:
    db: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)

    @router.post("/device", status_code=status.HTTP_200_OK,
                 response_model=schema_res.DeviceSchemaBase)
    async def generate_device(self):
        """
        Генерация и добавление в БД нового устройства
        """
        new_device = await DeviceORM.generate_device(db=self.db)

        return dict(new_device)


@cbv(router)
class AnalysisDataView:


    db: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
    syn_db: sqlalchemy.orm.session.Session = Depends(sync_session_maker)


    @router.get("/load_init_data",
                status_code=status.HTTP_201_CREATED)
    def load_init_data(self):

        with self.syn_db() as session:
            stmt = select(InfoDevice).limit(1)
            res = session.execute(stmt)
            is_empty = res.first()

            if is_empty:
                session.bulk_save_objects(bulk_new_devices)
                session.bulk_save_objects(bulk_new_info_device)
            # db.commit()
        return {"result": "success"}


    @router.get("/statistic",
                status_code=status.HTTP_200_OK,
                response_model=Optional[schema_res.AnalysisDataOneDeviceResponse]
                )
    async def device_statistic(self,
                               device_id: UUID,
                               from_datetime: Optional[datetime] = None,
                               to_datetime: Optional[datetime] = None):
        """
        Реализация получения статистики по конкретному устройству за период времени.

        :param device_id: идентификатор устройства
        :param from_datetime: начало временного периода
        :param to_datetime: конец временного периода
        """

        result = await InfoDeviceORM.get_statistic_one_devices(db=self.db,
                                                               from_datetime=from_datetime,
                                                               to_datetime=to_datetime,
                                                               device_id=device_id)
        if result is None:
            return None
        return result._asdict()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             db=Depends(get_async_session)):
    """
    Реализация real-time обновления статистики (общая по устройствам статистика).
    Если необходимо получить данные за период конкретного устройства (архивные данные), то
    для этого можно воспользоваться запросом `http://127.0.0.1:8000/data/statistic`

    :param websocket: websocket-объект
    :param db: объект AsyncGenerator для создания ассинхронной сессии базы данных.
    """
    schema_response = schema_res.AnalysisDataAllDeviceWebsocketResponse

    await websocket.accept()

    while True:
        response = await TaskResultORM.get_celery_result(db=db)

        response = response._asdict()
        response = pickle.loads(response['result'])
        response = schema_response(root=response).model_dump_json()

        await websocket.send_text(data=response)
        await asyncio.sleep(15)
