from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, TIMESTAMP, func,Double, JSON, Enum as SQLEnum, ForeignKey
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.product_image import ProductImage
    from app.models.testimonial import Testimonial

from app.configs.db import Base

class ConditionEnum(str, Enum):
    USED = "used"
    NEW = "new"
    REPACK = "repack"

class Product(Base):
    
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Double(10,2), nullable=False, default=0.0)
    specifications: Mapped[dict] = mapped_column(JSON, default=dict)
    
    rating: Mapped[float] = mapped_column(Double(3,2), default=0.0)
    condition: Mapped[str] = mapped_column(
        SQLEnum(
            ConditionEnum,
            name="product_condition",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=ConditionEnum.NEW,
        nullable=False
    ),
    
    category_id: Mapped[str] = mapped_column(
        ForeignKey(
            "categories.id",
            ondelete="CASCADE"
        ), 
        nullable=False
    )

    category: Mapped["Category"] = relationship(
        back_populates="products"
    )
    images: Mapped[list["ProductImage"]] = relationship()
    testimonals: Mapped[list["Testimonial"]] = relationship(
        back_populates="product"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )