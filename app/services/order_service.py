from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access import get_current_user
from app.models import OrderModel
from app.models.order_model import OrderStatus
from app.raises.raize_user_services import _not_found_order
from app.repo.order_repo import OrderRepository
from app.schemas.order_schemas import OrderCreateSchemaReq, OrderPatchStatusSchemaReq
from app.services.base_services import BaseServices
from app.core.db_connector import get_db


class OrderServices(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_order = OrderRepository(self.session)

    async def create_order(self, create_order_schema: OrderCreateSchemaReq) -> str:
        result = await self.repo_order.create_order(create_order_schema, get_current_user().id, OrderStatus.PENDING)
        await self.session.commit()
        return result

    async def get_order(self, order_id: int) -> OrderModel | None:
        result = await self.repo_order.get_order_user(order_id, get_current_user().id)
        if result is None:
            raise _not_found_order(order_id)
        return result

    async def update_status_order(self, order_id: int, update_schema: OrderPatchStatusSchemaReq) -> OrderModel:
        result = await self.repo_order.update_status_order(order_id, get_current_user().id, update_schema)
        await self.session.commit()
        return result

    async def get_all_order_user(self, user_id: int) -> List[OrderModel] | None:
        result = await self.repo_order.get_all_orders_user(user_id)
        return result


async def order_services(session: AsyncSession = Depends(get_db)) -> OrderServices:
    return OrderServices(session)
