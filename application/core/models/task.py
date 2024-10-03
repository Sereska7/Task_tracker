from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from application.core.models.base import Base
if TYPE_CHECKING:
    from application.core.models import Project, User


class TaskStatus(Enum):
    PENDING = 'Ожидание'
    IN_PROGRESS = 'В работе'
    COMPLETED = 'Выполнено'


class Task(Base):

    name: Mapped[str] = mapped_column(String(60))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    description: Mapped[str] = mapped_column(String(255))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    contractor: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), nullable=False)

    user: Mapped["User"] = relationship(back_populates="task")
    project: Mapped["Project"] = relationship(back_populates="task")