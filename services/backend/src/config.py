# Standard Library imports
import os

# Core FastAPI imports

# Third-party imports
from pydantic_settings import BaseSettings, SettingsConfigDict

# App imports


FILENAME_ENV = ".env"
PATH_WORKDIR = os.getcwd()
PATH_ENV = os.path.abspath("../../") + f"/{FILENAME_ENV}"

print(f"PATH_WORKDIR: {PATH_WORKDIR}")
print(f"PATH_ENV: {PATH_ENV}")


class Config(BaseSettings):
    FASTAPI_CONFIG: str
    DEBUG: bool = False

    # FastAPI
    FASTAPI_PROJECT_NAME: str
    FASTAPI_HOST: str
    FASTAPI_PORT: int
    FASTAPI_AUTH_SECRET: str

    # PostgreSQL
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_LOCALHOST: str
    PG_PORT: str
    PG_NAME: str

    # Redis
    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASES: int
    REDIS_DB: int

    # Celery
    # CELERY_BROKER_URL: str
    # CELERY_RESULT_BACKEND: str

    @property
    def PG_DATABASE_URL(self):
        # DSN
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return (f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}"
                f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}")

    @property
    def PG_SYNC_DATABASE_URL(self):
        # DSN
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return (f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}"
                f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}")

    @property
    def REDIS_DATABASE_URL(self):
        # redis://:password@hostname:port/db_number
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_BROKER_URL(self):
        return self.REDIS_DATABASE_URL

    @property
    def CELERY_RESULT_BACKEND(self):
        # return self.REDIS_DATABASE_URL
        return (f"db+postgresql://{self.PG_USER}:{self.PG_PASSWORD}"
                f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}")

    model_config = SettingsConfigDict(env_file=PATH_ENV,
                                      env_file_encoding='utf-8',
                                      extra='allow')


class DevelopmentConfig(Config):
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=f"{PATH_ENV}_dev",
                                      env_file_encoding='utf-8',
                                      extra='allow')


class ProductionConfig(Config):
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=PATH_ENV,
                                      env_file_encoding='utf-8',
                                      extra='allow')


config_manager = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)


def get_settings() -> BaseSettings:

    settings = Config()
    match settings.FASTAPI_CONFIG:
        case "dev":
            return DevelopmentConfig()
        case "prod":
            return ProductionConfig()


settings: BaseSettings = get_settings()

print(f"PG_DATABASE_URL:: {settings.PG_DATABASE_URL}")
