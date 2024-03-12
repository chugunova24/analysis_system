# Standard Library imports
from typing import AsyncGenerator

# Core FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Third-party imports
import uvicorn

# App imports
from src.config import settings
from src.data.queries.orm import InfoDeviceORM

"""

    Место подключения всех модулей приложения.

"""


# Инициализация приложения
app = FastAPI(
    title=settings.FASTAPI_PROJECT_NAME
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Маршрут-healthcheck для запущенного сервера
@app.get("/ping")
def ping():
    return {"ping": "pong!"}


# Routers
import src.routers


if __name__ == "__main__":
    uvicorn.run("src.main:app",
                host=settings.FASTAPI_HOST,
                reload=True,
                port=settings.FASTAPI_PORT)
