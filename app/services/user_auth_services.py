import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic.v1 import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.raises.raize_user_services import _not_found_user, _wrong_password
from app.repo.user_repo import UserRepository
from app.schemas.auth_schemas import TokenAccessSchemaRes, TokenDataPayloadSchema
from app.schemas.user_schemas import UserRegisterSchemaReq
from app.services.base_services import BaseServices
from app.utils.auth_utils import AuthUtils
from app.core.db_connector import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_bearer = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


class UserAuthServices(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_user = UserRepository(self.session)

    async def register_user(self, register_schema: UserRegisterSchemaReq) -> str:
        # Создаем пользователя
        self.log.info("register_user")
        find_user = await self.repo_user.find_user_email(register_schema.email)
        if find_user is not None:
            # Нельзя создать одинакового юзера по мэйлу
            self.log.error(f"User with email: {register_schema.email} register")
            raise _not_found_user(str(register_schema.email))
        register_schema.hashed_password = await AuthUtils.hash_password(register_schema.hashed_password)
        new_user = await self.repo_user.create_user(
            email=register_schema.email,
            hashed_password=register_schema.hashed_password,
            name=register_schema.name
        )
        await self.session.commit()
        return f"User {new_user.email} created"

    async def login_user(self, user_email: str, user_password_hash: str) -> TokenAccessSchemaRes:
        # Простой логин юзера. В случае успеха получим токены
        self.log.info(f"Try login user {user_email}")
        user_db = await self.repo_user.find_user_email(EmailStr(user_email))
        if user_db is None:
            self.log.error("User not found")
            raise _not_found_user("User not found")
        self.log.info(f"Find user email: {user_email}")
        if not await AuthUtils.verify_password(user_password_hash, user_db.hashed_password):
            self.log.warning("Wrong password")
            raise _wrong_password("Wrong password")
        return AuthUtils.create_tokens(TokenDataPayloadSchema.model_validate(user_db))

def user_auth_services(session: AsyncSession = Depends(get_db)) -> UserAuthServices:
    return UserAuthServices(session)