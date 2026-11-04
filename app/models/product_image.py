from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP, func, Enum as SQLEnum, ForeignKey
from datetime import datetime
from enum import Enum

from app.configs.db import Base

class ImageEnum(str, Enum):
    THUMB = "thumb"
    IMAGE = "image"

class ProductImage(Base):
    
    __tablename__ = "product_images"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    url: Mapped[str] = mapped_column(Text, nullable=False)
    public_id: Mapped[str] = mapped_column(Text, nullable=False)
    
    image_type: Mapped[str] = mapped_column(
        SQLEnum(
            ImageEnum,
            name="product_image_type",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        )
    ),
    
    product_id: Mapped[str] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )