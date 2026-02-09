import enum
import os

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker
from faststream.kafka.fastapi import KafkaRouter

from app.schemas.kafta_schema import MessageKafka

broker = KafkaBroker(f"{os.environ.get("KAFKA_HOST")}:{os.environ.get("KAFKA_PORT")}")
router = KafkaRouter(f"{os.environ.get("KAFKA_HOST")}:{os.environ.get("KAFKA_PORT")}")
app = FastStream(broker)


class Topics(enum.Enum):
    test_topic = "test_topic"


@broker.subscriber(Topics.test_topic.value, auto_offset_reset="earliest")
async def handle_message(msg: MessageKafka, logger: Logger):
    from app.interfaces.observer import EventManager, CeleryObserver
    logger.info(f"Received message: {msg}")
    event_manager = EventManager()
    event_manager.attach(CeleryObserver())
    await event_manager.publish_event(msg.type_order, msg.data)
    logger.info(f"Processing final")



if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())