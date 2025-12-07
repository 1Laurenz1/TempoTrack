from sqlalchemy import (
    Integer,
    String,
    BigInteger,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.entities.user import User

from typing import Optional


class UserModel(Base, TimeStampMixin):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )
    
    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
        index=True
    )
    email: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )
    password: Mapped[str] = mapped_column(
        String(256)
    )
    
    first_name: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True
    )
    tg_username: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True
    )
    telegram_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        unique=True,
        index=True
    )
    
    schedules_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    main_schedule: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        default=None,
    )
    
    
    @hybrid_property
    def is_active(self) -> bool:
        return self.schedules > 0
    
    @hybrid_property
    def full_name(self) -> str: 
        return f"{self.first_name} {self.last_name}"