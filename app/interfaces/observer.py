import logging

from app.schemas.kafta_schema import MessageKafka, TypeMessageKafka
from app.workers.consumer_faststream import Topics, broker


class EventManager:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    async def publish_event(self, event_type: TypeMessageKafka, data: str):
        for observer in self._observers:
            await observer.handle(event_type, data)

    def remove_observer(self, observer):
        self._observers.remove(observer)


class KafkaObserver:
    def __init__(self):
        self.broker = broker

    async def handle(self, event_type: TypeMessageKafka, data: str):
        topic = None
        if event_type == TypeMessageKafka.CELERY_TASK_1:
            topic = Topics.test_topic.value
        message = MessageKafka(data=data, type_order=event_type)
        async with self.broker:
            await self.broker.publish(message.model_dump(mode="json"), topic=topic)
        logging.info(f"[KafkaObserver] send in Kafka: {event_type}")


class CeleryObserver:
    async def handle(self, event_type: TypeMessageKafka, data: str):
        # Отправляем в Celery
        if event_type == TypeMessageKafka.CELERY_TASK_1:
            from app.workers.tasks import test_task
            test_task.delay(data)
        logging.info(f"[CeleryObserver] send in Celery: {event_type}")
