# Standard Library imports

# Core FastAPI imports

# Third-party imports
from sqlalchemy.orm import DeclarativeBase

# App imports


"""

    Базовый класс для моделей данных.
    Импорт готовых моделей данных.

"""


# Базовый класс для всех моделей данных, который собирает metadata
# со всех моделей.
class Base(DeclarativeBase):
    pass

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """
            Relationships не используются в repr(), т.к. могут вести к
            неожиданным подгрузкам
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


# Импорт моделей данных
from src.users import models as users_models
from src.data import models as data_models
