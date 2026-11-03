from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
from typing import Literal

class ProductImageDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
       
    uid: UUID = Field(default_factory=uuid4, alias="id")
    product: UUID
    
    image_type: Literal["image", "thumb"] = "image"
    
    url: str 
    public_id: str 
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))