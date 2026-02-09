import urllib
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from google.oauth2 import id_token

import aiohttp
import jwt
from passlib.context import CryptContext
import bcrypt
from google.auth.transport import requests as google_requests

from app.core.settings import settings
from app.raises.raize_user_services import _unauthorized as un
from app.schemas.auth_schemas import TokenAccessSchemaRes, TokenDataPayloadSchema
from app.schemas.google_api_schemas import ParamQueryLinkGoogleSchema, SchemaBodyGoogleGetToken, \
    SchemaResponseGoogleToken, SchemaVerifyOauth2TokenResponse


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
            payload = TokenDataPayloadSchema(**decoded)
            if datetime.now(timezone.utc).timestamp() > payload.exp:
                raise un(f"Legacy token")
            return TokenDataPayloadSchema(**decoded)

        except jwt.exceptions.ExpiredSignatureError:
            raise un("Token expired")
        except jwt.exceptions.InvalidTokenError as e:
            raise un(f"Invalid token")

    @staticmethod
    async def generate_google_link_oauth2() -> str:
        query_param = ParamQueryLinkGoogleSchema(client_id=settings.OAUTH_GOOGLE_CLIENT_ID,
                                                 redirect_uri=settings.GOOGLE_AUTH_CALLBACK_LINK).model_dump()
        query_string = urllib.parse.urlencode(query_param, quote_via=urllib.parse.quote)
        return f"{settings.GOOGLE_AUTH_MAIN_LINK}{query_string}"

    @staticmethod
    async def get_google_user_id(code: str) -> SchemaVerifyOauth2TokenResponse:
        async with aiohttp.ClientSession() as session:
            data = SchemaBodyGoogleGetToken(code=code, redirect_uri=settings.GOOGLE_AUTH_CALLBACK_LINK).model_dump()
            async with session.post(url=settings.GOOGLE_APIS_TOKEN, data=data) as response:
                try:
                    if response.status == 200:
                        response_data = await response.json()
                        res = SchemaResponseGoogleToken(**response_data)
                        id_info = id_token.verify_oauth2_token(
                            res.id_token,
                            google_requests.Request(),
                            settings.OAUTH_GOOGLE_CLIENT_ID
                        )
                        return SchemaVerifyOauth2TokenResponse(**id_info)
                    else:
                        raise HTTPException(status_code=400, detail=f"Error get user from google")
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=f"Invalid token: {str(e)}")
