from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.core.models.base import Base

if TYPE_CHECKING:
    from application.core.models import Task


class PositionType(Enum):
    DEVELOPER = 'Developer'
    MANAGER = 'Manager'
    TESTER = 'Tester'


class User(Base):

    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[str] = mapped_column()
    position: Mapped[PositionType] = mapped_column(SQLEnum(PositionType), nullable=False)
    is_director: Mapped[bool] = mapped_column(default=False)

    task: Mapped["Task"] = relationship(back_populates="user")
