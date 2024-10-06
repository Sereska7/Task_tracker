from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.core.models.base import Base
from application.utils.emun_types import PositionType

if TYPE_CHECKING:
    from application.core.models import Task


# Модель пользователя
class User(Base):
    """
    Класс модели User представляет пользователя системы с полями для имени,
    email, хешированного пароля, позиции в компании и указанием, является ли
    пользователь директором.
    """

    # Поле для хранения имени пользователя, длина строки ограничена 30 символами
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    # Поле для хранения email пользователя, длина строки ограничена 50 символами, уникально
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Поле для хранения хеша пароля пользователя
    hash_password: Mapped[str] = mapped_column(nullable=False)

    # Поле для хранения позиции пользователя, использует перечисление PositionType
    position: Mapped[PositionType] = mapped_column(
        SQLEnum(PositionType), nullable=False
    )

    # Поле для указания, является ли пользователь директором (по умолчанию False)
    is_director: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Отношение "многие ко многим" с задачами, созданными пользователем
    task: Mapped["Task"] = relationship(back_populates="user")
