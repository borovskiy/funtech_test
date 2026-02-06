from typing import Optional

from app.schemas.base_schema import BaseModelSchema


class TokenAccessSchemaRes(BaseModelSchema):
    access_token: str

class TokenAccessSchemaReq(BaseModelSchema):
    email: str
    hashed_password: str

class TokenDataPayloadSchema(BaseModelSchema):
    email: str
    id: int
    exp: Optional[int] = None