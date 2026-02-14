import time

from app.schemas.order_schemas import OrderCreateSchemaRes
from app.workers.celery import celery_app


@celery_app.task
def test_task(payload: dict):
    data = OrderCreateSchemaRes(**payload)

    # Теперь у вас есть доступ через точку с поддержкой IDE
    print(f"Processing order: {data.id}")
    time.sleep(2)
    print(f"Order {data.id} processed")
    return True