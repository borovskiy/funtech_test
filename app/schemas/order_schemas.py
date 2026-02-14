from typing import List
from uuid import UUID

from app.models.order_model import OrderStatus
from app.schemas.base_schema import BaseModelSchema, BaseIdSchemaMixin, BaseCreatedAndUpdateSchemaMixin


class OrderCreateSchemaReq(BaseModelSchema):
    items: List[str]
    total_price: float


class OrderCreateSchemaRes(OrderCreateSchemaReq, BaseIdSchemaMixin, BaseCreatedAndUpdateSchemaMixin):
    id: UUID
    user_id: float
    status: OrderStatus

class OrderPatchStatusSchemaReq(BaseModelSchema):
    status: OrderStatus

class OrderPatchStatusSchemaRes(OrderCreateSchemaRes):
    ...