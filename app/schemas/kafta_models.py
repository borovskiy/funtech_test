import enum

from pydantic import BaseModel

class TypeMessageKafka(enum.Enum):
    CELERY_TASK_1 = "CELERY_TASK_1"
    CELERY_TASK_2 = "CELERY_TASK_2"

class MessageKafka(BaseModel):
    type_order: TypeMessageKafka
    data: dict
