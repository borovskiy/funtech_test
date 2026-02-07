from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.schemas.order_schemas import OrderCreateSchemaRes, OrderCreateSchemaReq, OrderPatchStatusSchemaReq
from app.services.order_service import OrderServices, order_services
from app.core.access import auth
from app.utils.cache_builders import order_key_builder, CacheNamespace

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=OrderCreateSchemaRes, status_code=201, dependencies=[Depends(auth)])
async def create_order(
        order_serv: Annotated[OrderServices, Depends(order_services)],
        data: OrderCreateSchemaReq
):
    """Создание ордера"""
    return await order_serv.create_order(data)


@router.get("/{order_id}", response_model=OrderCreateSchemaRes, status_code=200, dependencies=[Depends(auth)])
@cache(expire=60*20, key_builder=order_key_builder)
async def get_order(
        order_serv: Annotated[OrderServices, Depends(order_services)],
        order_id: int
):
    """Получение Одного ордера"""
    return await order_serv.get_order(order_id=order_id)


@router.patch("/{order_id}", status_code=201, response_model=OrderCreateSchemaRes, dependencies=[Depends(auth)])
async def update_status(
        order_serv: Annotated[OrderServices, Depends(order_services)],
        data: OrderPatchStatusSchemaReq,
        order_id: int

):
    """Обновление статуса ордера"""
    return await order_serv.update_status_order(order_id=order_id, update_schema=data)


@router.get("/user/{user_id}", status_code=201, response_model=List[OrderCreateSchemaRes], dependencies=[Depends(auth)])
async def get_orders_user(
        order_serv: Annotated[OrderServices, Depends(order_services)],
        user_id: int,
):
    """Получение всех ордеров юзера"""
    ## Я бы тут пагинацию добавил но в задаче небыло ничего. И вобще ограничение сделал без user_id
    ## Все ранво токен требуем - чей токен того и ордеры - или тогда уже админ функционал
    return await order_serv.get_all_order_user(user_id)
