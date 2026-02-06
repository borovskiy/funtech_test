import enum
from typing import List, Dict, Any, TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, JSON, Float, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from .user_model import UserModel


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"


class OrderModel(BaseModel):
    __tablename__ = "orders"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    items: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    user: Mapped["UserModel"] = relationship(back_populates="orders")
