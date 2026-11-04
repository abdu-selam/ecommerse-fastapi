from pydantic import BaseModel, ConfigDict, Field, EmailStr, SecretStr
from typing import Annotated, Literal
from datetime import datetime, UTC
from uuid import uuid4, UUID

class AdminDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    uid: UUID = Field(default_factory=uuid4, alias="id")
        
    name: str
    email: EmailStr
    password: SecretStr

    roll: Literal["owner", "admin"] = "owner"

    refresh_token: str | None = None
    refresh_created_at: datetime | None = None

    forgot_token: str | None = None
    forgot_created_at: datetime | None = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminLoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    email: EmailStr
    roll: Literal["owner", "admin"] = "owner"
