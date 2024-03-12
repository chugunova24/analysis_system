# Standard Library imports
import uuid
from datetime import datetime
from typing import Annotated

# Core FastAPI imports

# Third-party imports
from sqlalchemy.orm import mapped_column
from sqlalchemy import text, UUID

# App imports


"""

    Здесь создаем базовые типы данных, которые часто используются
    во всем проекте.

"""


int_pk = Annotated[int, mapped_column(primary_key=True,
                                      autoincrement=True)]

uuid_pk = Annotated[UUID, mapped_column(UUID(as_uuid=True),
                                        primary_key=True,
                                        default=uuid.uuid4)]

created_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]

updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow)]

counter = Annotated[int, mapped_column(nullable=False, default=0)]
