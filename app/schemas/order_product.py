from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from uuid import UUID, uuid4
from typing import Annotated

class OrderProductDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
   
    uid: UUID = Field(default_factory=uuid4, alias="id")
    product_id: UUID
    order_id: UUID

    price: Annotated[float, Field(gt=0)]
    amount: Annotated[float, Field(ge=1)]
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))