from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Double, TIMESTAMP, func, ForeignKey
from datetime import datetime

from app.configs.db import Base

class OrderProduct(Base):
    
    __tablename__ = "order_products"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    product_id: Mapped[str] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    order_id: Mapped[str] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    price: Mapped[float] = mapped_column(Double(10,2), nullable=False, default=0.0)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )