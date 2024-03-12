# Standard Library imports

# Core FastAPI imports
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

# Third-party imports
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import EmailType

# App imports
from src.db import base as b
from src.db import types as t


"""

    Модели данных модуля users.

"""


class User(SQLAlchemyBaseUserTableUUID, b.Base):
    __tablename__ = "user"

    id: Mapped[t.uuid_pk]
    email = mapped_column(EmailType, nullable=False, unique=True)
    hashed_password = mapped_column(String(1024), nullable=False)
    username = mapped_column(String(200), nullable=False)
    firstName = mapped_column(String(200), nullable=True)
    lastName = mapped_column(String(200), nullable=True)
    registered_at: Mapped[t.created_at]
    is_active = mapped_column(Boolean, nullable=False, default=False)
    is_superuser = mapped_column(Boolean, nullable=False, default=False)
    is_verified = mapped_column(Boolean, nullable=False, default=False)
    role_id = mapped_column(ForeignKey("role.id"), nullable=False, default=1)

    # role: Mapped["Role"] = relationship(back_populates="user")
    # comments: Mapped[List["Comment"]] = relationship(back_populates="user")


class Role(b.Base):
    __tablename__ = "role"

    id: Mapped[t.int_pk]
    name = mapped_column(String(200), nullable=False, unique=True)
    # permissions = mapped_column(JSON, nullable=False)

    # user: Mapped[List["User"]] = relationship(back_populates="role")
