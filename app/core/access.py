from contextvars import ContextVar
from typing import Optional

from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from app.schemas.auth_schemas import TokenDataPayloadSchema
from app.utils.auth_utils import AuthUtils

_current_user: ContextVar[Optional[TokenDataPayloadSchema]] = ContextVar("current_user", default=None)

def set_current_user(user: TokenDataPayloadSchema) -> None:
    _current_user.set(user)

def get_current_user() -> TokenDataPayloadSchema:
    user = _current_user.get()
    return user

auth_scheme = HTTPBearer(auto_error=False)

async def get_token(credentials: Optional[HTTPAuthorizationCredentials] = Security(auth_scheme)) -> str:
    """
    Извлекает токен из Authorization header, выбрасывает 401 если нет.
    """
    if not credentials or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    return credentials.credentials

async def auth(token: str = Depends(get_token)):
    user_payload = AuthUtils.verify_token(token)
    set_current_user(user_payload)
