from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_repository import BaseRepo
from app.models.user_model import UserModel


class UserRepository(BaseRepo[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.user_model = UserModel

    async def create_user(self, email: EmailStr, hashed_password: str, name: str) -> UserModel | None:
        ##  Можно сделать проще  - через словарь сериализовывать, но тут не стал делать - внизу пример
        self.log.info(f"create_user")
        obj = UserModel(email=email, hashed_password=hashed_password, name=name)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def find_user_email(self, email: EmailStr) -> UserModel | None:
        self.log.info("find_user_email {email}")
        stmt = (
            select(self.user_model)
            .where(self.user_model.email == email)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def find_user_id(self, id_user: int) -> UserModel | Exception:
        self.log.info(f"find_user_id {id_user} ")
        stmt = (
            select(self.user_model)
            .where(self.user_model.id == id_user)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

        ...

    # Пример
    # async def create_one_obj_model(self, data: dict) -> ModelType:
    #     self.log.info(f"create_one_obj_model")
    #     model_fields = self.main_model.__table__.columns.keys()
    #     filtered_data = {k: v for k, v in data.items() if k in model_fields}
    #     obj = self.main_model(**filtered_data)
    #     self.session.add(obj)
    #     await self.session.flush()
    #     return obj
