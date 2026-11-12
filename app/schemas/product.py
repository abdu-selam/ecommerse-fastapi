from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, UTC
from uuid import UUID, uuid4
from typing import Annotated, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product_image import ProductImage

class ProductDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
   
    uid: UUID = Field(default_factory=uuid4, alias="id")
    name: str
    description: str | None = None
    price: Annotated[float, Field(gt=0)]
    specifications: dict = Field(default_factory=dict)

    rating: float = Field(default_factory=lambda: 0.0, ge=0, le=5)
    condition: Literal["used", "new", "repack"] = "new"
    
    category_id: UUID
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class ProductResponseImage(BaseModel):
    iid: Annotated[str, Field(alias="id")]
    url: str

class ProductsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price: float
    category: Annotated[str, Field(alias="category_id")]
    pid: Annotated[str, Field(alias="id")]
    rating: float
    images: list[ProductResponseImage]

class ProductResponseCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pid: Annotated[str, Field(alias="id")]
    image_url: str
    name: str

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
       
    pid: Annotated[str, Field(alias="id")]
    name: str
    description: str | None = None
    price: Annotated[float, Field(gt=0)]
    specifications: dict = Field(default_factory=dict)

    rating: float 
    condition: Literal["used", "new", "repack"]
    
    category: list[ProductResponseCategory]
    images: list[ProductResponseImage]
    
    created_at: datetime
    updated_at: datetime