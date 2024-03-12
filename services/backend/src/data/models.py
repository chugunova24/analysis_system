# Standard Library imports

# Core FastAPI imports

# Third-party imports
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

# App imports
from src.db import base as b
from src.db import types as t


"""

    Модели данных модуля data.

"""


# Таблица с информацией о зарегистрированных устройствах
class Device(b.Base):
    __tablename__ = "device"

    id: Mapped[t.uuid_pk]  # uuid устройства


# Таблица для данных, которые приходят с утройства в формате {x: float, y: float, z: float}
class InfoDevice(b.Base):
    __tablename__ = "info_device"

    id: Mapped[t.int_pk]  # id записи в БД
    device_id = mapped_column(ForeignKey("device.id"), nullable=False)  # uuid устройства
    created_at: Mapped[t.created_at]   # время создания записи в БД
    x: Mapped[float]  # абстрактное значение
    y: Mapped[float]
    z: Mapped[float]

    device = relationship("Device")
