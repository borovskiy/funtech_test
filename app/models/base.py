from enum import Enum

from sqlalchemy import func, Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """
    Основная модель с временем сохранения
    Можно делать миксином но тут не стал
    """
    created_at: Mapped[int] = mapped_column(
        BigInteger,
        server_default=func.extract('epoch', func.now()),
        nullable=False
    )
    updated_at: Mapped[int] = mapped_column(
        BigInteger,
        server_default=func.extract('epoch', func.now()),
        nullable=False
    )

    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, Enum):
                value = value.value
            result[c.name] = value
        return result
