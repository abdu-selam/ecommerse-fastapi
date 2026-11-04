from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, TIMESTAMP, func, Enum as SQLEnum
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order_product import OrderProduct

from app.configs.db import Base

class StatusEnum(str, Enum):
    SOLD = "sold"
    HOLD = "hold"
    UNPAID = "unpaid"
    
class OrderEnum(str, Enum):
    DELIVERED = "delivered"
    ONFIELD = "onfield"

class Order(Base):
    
    __tablename__ = "orders"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    status: Mapped[str] = mapped_column(
        SQLEnum(
            StatusEnum,
            name="order_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=StatusEnum.UNPAID,
        nullable=False
    ),
    status_update: Mapped[datetime] = mapped_column(TIMESTAMP)
    
    order_type: Mapped[str] = mapped_column(
        SQLEnum(
            OrderEnum,
            name="orders_type",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=OrderEnum.ONFIELD,
        nullable=False
    )
    
    user_name: Mapped[str] = mapped_column(String(30), nullable=False)
    user_email: Mapped[str] = mapped_column(String(50), nullable=False)
    user_tell: Mapped[str] = mapped_column(String(15), nullable=False)
    
    stripe_session_id: Mapped[str] = mapped_column(Text)
    receipt: Mapped[str] = mapped_column(Text)

    order_products: Mapped[list["OrderProduct"]] = relationship()
    
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )