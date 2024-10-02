from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.core.models.base import Base

if TYPE_CHECKING:
    from application.core.models import Task


class Project(Base):

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))

    task: Mapped["Task"] = relationship(back_populates="project")
