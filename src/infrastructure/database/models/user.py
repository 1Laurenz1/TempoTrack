from sqlalchemy import (
    Integer,
    String,
    BigInteger,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import BYTEA

from src.infrastructure.database.session import Base
from src.infrastructure.database.mixins.time_stamp_mixin import TimeStampMixin

from src.domain.entities.user import User

from typing import Optional, List


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
    password: Mapped[bytes] = mapped_column(
        BYTEA(256),
        nullable=False
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
    
    schedules: Mapped[List['ScheduleModel']] = relationship(
        'ScheduleModel',
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    items: Mapped[List["ScheduleItemsModel"]] = relationship(
        back_populates="user"
    )
    
    
    @hybrid_property
    def is_active(self) -> bool:
        return self.schedules_count > 0
    
    @hybrid_property
    def full_name(self) -> str: 
        return f"{self.first_name} {self.last_name}"