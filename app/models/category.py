from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, TIMESTAMP, func, JSON
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import Product

from app.configs.db import Base

class Category(Base):
    
    __tablename__ = "categories"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_public_id: Mapped[str] = mapped_column(Text, nullable=False)
    
    specifications: Mapped[list] = mapped_column(JSON, default=list)

    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )