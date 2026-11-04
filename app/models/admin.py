from app.configs.db import Base
from sqlalchemy import String, Text, Enum as SQLEnum, func, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from enum import Enum
from datetime import datetime

class RollEnum(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"

class Admin(Base):
    
    __tablename__ = "admins"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False
    )
    password: Mapped[str] = mapped_column(Text, nullable=False)

    roll: Mapped[RollEnum] = mapped_column(
        SQLEnum(
            RollEnum,
            name="admin_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=RollEnum.OWNER,
        nullable=False
    )

    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)
    refresh_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    forgot_token: Mapped[str] = mapped_column(Text, nullable=True)
    forgot_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp()
    )