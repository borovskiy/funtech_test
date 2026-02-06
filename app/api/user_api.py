from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.auth_schemas import TokenAccessSchemaReq, TokenAccessSchemaRes
from app.schemas.user_schemas import UserRegisterSchemaReq
from app.services.user_auth_services import UserAuthServices, user_auth_services

router = APIRouter(
    prefix="/user_auth",
    tags=["User auth"],
)


@router.post("/register", status_code=201)
async def register_user(
        user_auth_serv: Annotated[UserAuthServices, Depends(user_auth_services)],
        model_user: UserRegisterSchemaReq,
):
    """Register user"""
    return await user_auth_serv.register_user(register_schema=model_user)

@router.post("/token", status_code=201, response_model=TokenAccessSchemaRes)
async def get_token(
        user_auth_serv: Annotated[UserAuthServices, Depends(user_auth_services)],
        model_user: TokenAccessSchemaReq,
):
    """Create auth token"""
    return await user_auth_serv.login_user(user_email=model_user.email, user_password_hash=model_user.hashed_password)
