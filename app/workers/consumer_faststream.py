import enum

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker
from faststream.kafka.fastapi import KafkaRouter
from app.workers.tasks import test_task
from app.schemas.kafta_models import MessageKafka

broker = KafkaBroker("localhost:9094")
router = KafkaRouter("localhost:9094")
app = FastStream(broker)


class Topics(enum.Enum):
    test_topic = "test_topic"


# Подписываемся на топик 'test-topic'
@broker.subscriber(Topics.test_topic.value, auto_offset_reset="earliest")
async def handle_message(msg: MessageKafka, logger: Logger):
    logger.info(f"Received message: {msg}")
    test_task.delay(msg.data)
    print(f"Processing data: {msg.data}")
    print(f"Processing type_order : {msg.type_order}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())