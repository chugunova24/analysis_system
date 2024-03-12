# Standard Library imports

# Core FastAPI imports
from fastapi import APIRouter
from fastapi_restful.cbv import cbv

# Third-party imports

# App imports


"""

    Обработка маршрутов модуля users.

"""


router = APIRouter()


# Можно удалить этот класс. Это class-based view
@cbv(router)
class UserView:

    @router.get("/ping/{name}")
    async def ping(self, name: str):
        return {"ping": f"pong, {name}!"}
