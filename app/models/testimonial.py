from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP, func, Double, ForeignKey
from datetime import datetime

from app.configs.db import Base

class Testimonial(Base):
    
    __tablename__ = "testimonials"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    product: Mapped[str] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    stars: Mapped[float] = mapped_column(Double(3,2), default=5.0, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )