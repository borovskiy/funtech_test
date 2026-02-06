from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext
import bcrypt

from app.core.settings import settings
from app.raises.raize_user_services import _unauthorized as un
from app.schemas.auth_schemas import TokenAccessSchemaRes, TokenDataPayloadSchema


class AuthUtils:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @staticmethod
    async def hash_password(plain: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(plain.encode(), salt).decode()

    @staticmethod
    async def verify_password(plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    @staticmethod
    def create_access_token(data: "TokenDataPayloadSchema") -> TokenAccessSchemaRes:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.VERIFY_TOKEN_TTL_MIN)
        data.exp = int(expire.timestamp())
        return TokenAccessSchemaRes(access_token=jwt.encode(
            data.model_dump(),
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALG
        ))

    @staticmethod
    def create_tokens(data: TokenDataPayloadSchema) -> TokenAccessSchemaRes:
        return AuthUtils.create_access_token(data)

    # --- Проверка токена ---
    @staticmethod
    def verify_token(token: str, refresh: bool = False) -> "TokenDataPayloadSchema":
        try:
            secret = (
                settings.JWT_SECRET_REFRESH if refresh else settings.JWT_SECRET
            )

            decoded = jwt.decode(
                token,
                secret,
                algorithms=[settings.JWT_ALG]
            )
            return TokenDataPayloadSchema(**decoded)

        except jwt.exceptions.ExpiredSignatureError:
            raise un("Token expired")
        except jwt.exceptions.InvalidTokenError as e:
            raise un(f"Invalid token")
