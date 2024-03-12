# Standard Library imports

# Core FastAPI imports

# Third-party imports

# App imports
from src.main import app
from src.users.routers import router as users_router
from src.auth.routers import router as auth_router
from src.auth.schemas import UserRead, UserCreate
from src.auth.manager import auth_backend, fastapi_users
from src.data.routers import router as data_router


"""

    Место подключения всех маршрутизаторов к приложению.

"""


# Auth
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(auth_router,
                   prefix="/auth",
                   tags=["auth"])
app.include_router(data_router,
                   prefix="/data",
                   tags=["data"])


# Users
app.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
