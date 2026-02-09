import enum
from typing import Optional

from pydantic import BaseModel

from app.core.settings import settings


class TypeScopeGoogle(enum.Enum):
    openid = "openid"
    profile = "profile"
    email = "email"

class GrantTypeGoogle(enum.Enum):
    authorization_code = "authorization_code"


class ParamQueryLinkGoogleSchema(BaseModel):
    client_id: Optional[str]
    redirect_uri: str
    response_type: str = "code"
    scope: str = " ".join([TypeScopeGoogle.openid.name, TypeScopeGoogle.profile.name, TypeScopeGoogle.email.name])

class SchemaBodyGoogleGetToken(BaseModel):
    client_id: str = settings.OAUTH_GOOGLE_CLIENT_ID
    client_secret: str =settings.OAUTH_GOOGLE_CLIENT_SECRET
    code: str
    redirect_uri: str
    grant_type: str = GrantTypeGoogle.authorization_code.name


class SchemaResponseGoogleToken(BaseModel):
    access_token: str
    expires_in: int
    scope: str
    id_token: str
    token_type: str

class SchemaVerifyOauth2TokenResponse(BaseModel):
    email_verified:bool
    name:str
    email:str