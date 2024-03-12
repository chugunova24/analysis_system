# Standard Library imports
from uuid import UUID

# Core FastAPI imports

# Third-party imports
from pydantic import BaseModel

# App imports


"""

    Схемы запросов для модуля data

"""


datetime_format = '%Y-%m-%d %H:%M:%S'


class InfoSchemaRequest(BaseModel):
    x: float
    y: float
    z: float


class TEST_InfoSchemaRequest(InfoSchemaRequest):
    device_id: UUID
