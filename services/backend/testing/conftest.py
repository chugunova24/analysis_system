# Standard Library imports

# Core FastAPI imports

# Third-party imports

# App imports
from src.config import Config


"""

Здесь содержится тестовая конфигурация для ВСЕХ тестов (в том числе фикстуры).

"""


class TestingConfig(Config):
    DEBUG: bool = True
    TESTING: bool = True

    # TESTING database
    TEST_PG_DATABASE_URL: str
    TEST_REDIS_DATABASE_URL: str


configtest = TestingConfig()
