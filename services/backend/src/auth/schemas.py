# Standard Library imports
import uuid

# Core FastAPI imports
from fastapi_users import schemas

# Third-party imports

# App imports


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
