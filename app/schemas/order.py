from pydantic import BaseModel, ConfigDict, Field, EmailStr
from uuid import UUID, uuid4
from datetime import datetime, UTC
from typing import Literal

class OrderDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True, frozen=True)
       
    uid: UUID = Field(default_factory=uuid4, alias="id")
        
    status: Literal["sold", "hold", "unpaid"] = "unpaid"
    status_update: datetime
    
    order_type: Literal["delivered", "onfield"] = "onfield"
    
    user_name: str | None = None
    user_email: EmailStr | None = None
    user_tell: str | None = None
    
    stripe_session_id: str | None = None
    receipt: str | None = None
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))