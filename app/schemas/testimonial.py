from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from uuid import UUID, uuid4

class TestimonialDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
   
    uid: UUID = Field(default_factory=uuid4, alias="id")

    name: str
    message: str 
    stars: float = Field(default_factory=lambda: 0.0, ge=0, le=5)
    
    product_id: UUID
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))