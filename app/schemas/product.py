from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from uuid import UUID, uuid4
from typing import Annotated, Literal

class ProductDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
   
    uid: UUID = Field(default_factory=uuid4, alias="id")
    name: str
    description: str | None = None
    price: Annotated[float, Field(gt=0)]
    specifications: dict = Field(default_factory=dict)

    rating: float = Field(default_factory=lambda: 0.0, ge=0, le=5)
    condition: Literal["used", "new", "repack"] = "new"
    
    category: UUID
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))