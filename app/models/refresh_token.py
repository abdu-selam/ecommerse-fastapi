from app.configs.db import Base
from sqlalchemy import String, Text,  func, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.admin import Admin

class RefreshToken(Base):
    
    __tablename__ = "refresh_tokens"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    token: Mapped[str] = mapped_column(Text, nullable=False)
    admin_id: Mapped[str] = mapped_column(
        ForeignKey(
            "admins.id",
            ondelete="CASCADE"
        ), 
        nullable=False
    )

    admin: Mapped["Admin"] = relationship()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp()
    )