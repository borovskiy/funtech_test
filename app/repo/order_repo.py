from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_repository import BaseRepo
from app.models.order_model import OrderModel, OrderStatus
from app.schemas.order_schemas import OrderCreateSchemaReq, OrderPatchStatusSchemaReq


class OrderRepository(BaseRepo[OrderModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.order_model = OrderModel

    async def create_order(self, data: OrderCreateSchemaReq, user_id: int, status: OrderStatus):
        ##  Можно сделать проще через словарь сериализовывать но тут не стал делать - внизу пример
        self.log.info(f"create_order")
        obj = OrderModel(**data.model_dump())
        obj.user_id = user_id
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_order_user(self, order_id: int, user_id: int) -> OrderModel | None:
        self.log.info("get_order_user %s ", order_id)
        stmt = (
            select(self.order_model)
            .where(
                and_(
                    self.order_model.id == order_id,
                    self.order_model.user_id == user_id
                ))
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def update_status_order(self, order_id: int, user_id: int,
                                  update_schema: OrderPatchStatusSchemaReq) -> OrderModel | None:
        self.log.info("update_status_order %s ", order_id)

        stmt = (
            update(self.order_model)
            .where(
                and_(
                    self.order_model.id == order_id,
                    self.order_model.user_id == user_id,
                )
            )
            .values(**update_schema.model_dump())
            .returning(self.order_model)
        )

        result = await self.session.execute(stmt)
        updated_contact = result.scalar_one_or_none()

        await self.session.flush()
        return updated_contact


    async def get_all_orders_user(self, user_id: int):
        self.log.info("get_all_orders_user %s ", user_id)
        stmt = (
            select(self.order_model)
            .where(
                and_(
                    self.order_model.user_id == user_id
                ))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
