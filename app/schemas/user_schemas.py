from pydantic import EmailStr, Field

from app.schemas.base_schema import BaseModelSchema


class UserRegisterSchemaReq(BaseModelSchema):
    email: EmailStr | None = Field(default=None)
    hashed_password: str = Field(..., min_length=8)
    name: str
