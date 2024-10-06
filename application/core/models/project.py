from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.core.models.base import Base

if TYPE_CHECKING:
    from application.core.models import Task


# Модель проекта, связанная с задачами
class Project(Base):
    """
    Класс модели Project представляет проект с полями для имени, описания и
    установкой связи с задачами (Task).
    """

    # Поле для хранения имени проекта, длина строки ограничена 50 символами
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Поле для хранения описания проекта, длина строки ограничена 255 символами
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Связь один ко многим с таблицей Task, обратная связь на поле "project" в модели Task
    task: Mapped["Task"] = relationship(back_populates="project")
