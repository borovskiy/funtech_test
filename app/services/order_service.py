import hashlib
import json
from typing import List, TYPE_CHECKING

from fastapi import Depends
from fastapi_cache import FastAPICache
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access import get_current_user
from app.interfaces.observer import KafkaObserver
from app.models import OrderModel
from app.models.order_model import OrderStatus
from app.raises.raize_user_services import _not_found_order
from app.repo.order_repo import OrderRepository
from app.schemas.kafta_schema import TypeMessageKafka
from app.schemas.order_schemas import OrderCreateSchemaReq, OrderPatchStatusSchemaReq, OrderCreateSchemaRes
from app.services.base_services import BaseServices
from app.core.db_connector import get_db
from app.utils.cache_builders import get_key_order_cache


class OrderServices(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_order = OrderRepository(self.session)
        self.event_manager.attach(KafkaObserver())
        self.cache_backend = FastAPICache.get_backend()

    async def create_order(self, create_order_schema: OrderCreateSchemaReq) -> str:
        self.log.info(f"create_order")
        result = await self.repo_order.create_order(create_order_schema, get_current_user().id, OrderStatus.PENDING)
        data = OrderCreateSchemaRes(**result.as_dict())
        await self.session.commit()
        await self.event_manager.publish_event(event_type=TypeMessageKafka.CELERY_TASK_1, data=data.model_dump())
        return result

    async def get_order(self, order_id: str) -> OrderModel | None:
        self.log.info(f"get_order")
        result = await self.repo_order.get_order_user(order_id, get_current_user().id)
        if result is None:
            raise _not_found_order(order_id)
        return result

    async def update_status_order(self, order_id: str, update_schema: OrderPatchStatusSchemaReq) -> OrderModel:
        self.log.info(f"update_status_order")
        result = await self.repo_order.update_status_order(order_id, get_current_user().id, update_schema)
        await self.session.commit()
        await self.cache_backend.set(get_key_order_cache(order_id), OrderCreateSchemaRes(**result.as_dict()).model_dump_json().encode('utf-8'), expire=60 * 5)
        return result

    async def get_all_order_user(self, user_id: int) -> List[OrderModel] | None:
        result = await self.repo_order.get_all_orders_user(user_id)
        return result


async def order_services(session: AsyncSession = Depends(get_db)) -> OrderServices:
    return OrderServices(session)
