# Standard Library imports

# Core FastAPI imports
from fastapi import Depends, APIRouter

# Third-party imports

# App imports
from src.users.models import User
from src.auth.manager import current_active_user


router = APIRouter()


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """
    Маршрут для проверки защищенного пути.

    :param user: Текущий пользователь
    :return: Сообщение-приветсвие
    """
    return {"message": f"Hello {user.email}!"}
