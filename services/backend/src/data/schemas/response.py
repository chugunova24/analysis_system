# Standard Library imports
from datetime import datetime
from uuid import UUID

# Core FastAPI imports

# Third-party imports
from pydantic import ConfigDict, BaseModel, RootModel

# App imports


"""

    Схемы запросов для модуля data

"""


# Базовая схема ответа для таблицы InfoDevice
class InfoDeviceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class InfoSchemaResponse(InfoDeviceBase):
    id: int
    device_id: UUID
    created_at: datetime
    x: float
    y: float
    z: float


class InfoSchemaAll(InfoDeviceBase):
    device_id: UUID
    rows:  list["InfoSchemaResponse"]


class InfoDevicesResponse(InfoDeviceBase):
    lost_of_devices: list["InfoSchemaAll"]


# Базовая схема ответа для таблицы Device
class DeviceSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    device_id: UUID


class AnalysisDataSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    count: int

    min_x: float
    min_y: float
    min_z: float

    max_x: float
    max_y: float
    max_z: float

    sum_x: float
    sum_y: float
    sum_z: float

    mediana_x: float
    mediana_y: float
    mediana_z: float


class AnalysisDataOneDeviceResponse(AnalysisDataSchemaBase):
    device_id: UUID


class AnalysisDataOneDeviceWebsocketResponse(AnalysisDataSchemaBase):
    device_id: UUID


class AnalysisDataAllDeviceWebsocketResponse(RootModel):
    root: list["AnalysisDataOneDeviceWebsocketResponse"]
