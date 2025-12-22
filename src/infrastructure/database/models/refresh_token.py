from datetime import datetime
from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import BYTEA, BOOLEAN

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.entities.refresh_token import RefreshToken


class RefreshTokenModel(Base, TimeStampMixin):
    __tablename__ = 'refresh_sessions'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    token_hash: Mapped[bytes] = mapped_column(
        BYTEA,
        unique=True,
        nullable=False,
    )
    revoked: Mapped[bool] = mapped_column(
        BOOLEAN,
        nullable=False,
        default=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )