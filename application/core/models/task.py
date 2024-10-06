from typing import TYPE_CHECKING

from sqlalchemy import String, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from application.core.models.base import Base
from application.utils.emun_types import TypeTask, TaskStatus

if TYPE_CHECKING:
    from application.core.models import Project, User


# Модель задачи, связанная с проектом и пользователем
class Task(Base):
    """
    Класс модели Task представляет задачу с полями для имени, описания,
    дат начала и завершения, назначенного пользователя и связанного проекта.
    """

    # Поле для хранения имени задачи, длина строки ограничена 60 символами
    name: Mapped[str] = mapped_column(String(60), nullable=False)

    # Внешний ключ, указывающий на ID проекта
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    # Поле для хранения описания задачи, длина строки ограничена 255 символами
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Поле для даты начала задачи
    date_from: Mapped[date] = mapped_column(Date, nullable=False)

    # Поле для даты завершения задачи
    date_to: Mapped[date] = mapped_column(Date, nullable=False)

    # Внешний ключ, указывающий на ID исполнителя задачи (пользователь)
    contractor: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Тип задачи (например, разработка, тестирование и т.д.), обязательное поле
    type_task: Mapped[TypeTask] = mapped_column(SQLEnum(TypeTask), nullable=False)

    # Статус задачи (например, в ожидании, в процессе и т.д.), по умолчанию "PENDING"
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False
    )

    # Связь с моделью пользователя через отношение "многие ко многим"
    user: Mapped["User"] = relationship(back_populates="task")

    # Связь с моделью проекта через отношение "многие ко многим"
    project: Mapped["Project"] = relationship(back_populates="task")
