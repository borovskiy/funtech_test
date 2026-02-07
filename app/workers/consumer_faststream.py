import enum
import os
from typing import TYPE_CHECKING

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker
from faststream.kafka.fastapi import KafkaRouter

from app.workers.tasks import test_task
from app.schemas.kafta_schema import MessageKafka

broker = KafkaBroker(f"{os.environ.get("KAFKA_HOST")}:{os.environ.get("KAFKA_PORT")}")
router = KafkaRouter(f"{os.environ.get("KAFKA_HOST")}:{os.environ.get("KAFKA_PORT")}")
app = FastStream(broker)


class Topics(enum.Enum):
    test_topic = "test_topic"


# Подписываемся на топик 'test-topic'
@broker.subscriber(Topics.test_topic.value, auto_offset_reset="earliest")
async def handle_message(msg: MessageKafka, logger: Logger):
    from app.interfaces.observer import EventManager, CeleryObserver
    event_manager = EventManager()
    event_manager.attach(CeleryObserver())
    await event_manager.publish_event(msg.type_order, msg.data)
    logger.info(f"Received message: {msg}")
    test_task.delay(msg.data)
    print(f"Processing data: {msg.data}")
    print(f"Processing type_order : {msg.type_order}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())