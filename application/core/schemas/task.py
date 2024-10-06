from datetime import date

from fastapi import Form
from pydantic import BaseModel, EmailStr

from application.utils.emun_types import TypeTask, TaskStatus


# Базовая модель задачи, используемая для представления задачи
class SBaseTask(BaseModel):
    """
    Класс SBaseTask представляет базовую информацию о задаче.
    """
    name: str  # Имя задачи
    project_id: int  # Идентификатор проекта
    description: str  # Описание задачи
    date_from: date  # Дата начала задачи
    date_to: date  # Дата завершения задачи
    contractor: int  # Идентификатор ответственного пользователя
    type_task: str  # Тип задачи (например, "BUG", "FEATURE")
    status: str  # Статус задачи (например, "IN_PROGRESS", "COMPLETED")


# Модель для изменения информации о задаче
class SChangeTask(BaseModel):
    """
    Класс SChangeTask используется для изменения некоторых полей задачи.
    """
    description: str  # Обновленное описание задачи
    date_from: date  # Обновленная дата начала задачи
    date_to: date  # Обновленная дата завершения задачи


# Модель, представляющая основные данные задачи (без статуса)
class STask(BaseModel):
    """
    Класс STask представляет основные данные задачи, которые создаются или редактируются.
    """
    name: str  # Имя задачи
    project_id: int  # Идентификатор проекта
    description: str  # Описание задачи
    date_from: date  # Дата начала задачи
    date_to: date  # Дата завершения задачи
    contractor: int  # Идентификатор ответственного пользователя


# Модель для отображения задачи пользователя (с проектом и статусом)
class SMyTask(BaseModel):
    """
    Класс SMyTask представляет задачу пользователя с дополнительной информацией.
    """
    name: str  # Имя задачи
    project_name: str  # Название проекта
    description: str  # Описание задачи
    contractor_email: EmailStr  # Email исполнителя задачи
    date_from: date  # Дата начала задачи
    date_to: date  # Дата завершения задачи
    status: str  # Статус задачи (например, "IN_PROGRESS", "COMPLETED")


# Модель формы для создания задачи
class STaskCreateForm(BaseModel):
    """
    Класс STaskCreateForm используется для создания новой задачи через форму.
    """
    name: str  # Имя задачи
    project_id: int  # Идентификатор проекта
    description: str  # Описание задачи
    date_from: date  # Дата начала задачи
    date_to: date  # Дата завершения задачи
    contractor: int  # Идентификатор ответственного пользователя
    type_task: TypeTask  # Тип задачи (например, "BUG", "FEATURE")
    status: TaskStatus  # Статус задачи (например, "PENDING", "IN_PROGRESS")

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),  # Поле формы для имени задачи, обязательное
        project_id: int = Form(...),  # Поле формы для выбора проекта, обязательное
        description: str = Form(...),  # Поле формы для описания задачи, обязательное
        date_from: date = Form(...),  # Поле формы для даты начала задачи
        date_to: date = Form(...),  # Поле формы для даты завершения задачи
        contractor: int = Form(...),  # Поле формы для выбора исполнителя задачи
        type_task: TypeTask = Form(...),  # Поле формы для выбора типа задачи
        status: TaskStatus = Form(...),  # Поле формы для выбора статуса задачи
    ):
        """
        Метод для создания объекта формы, который будет использоваться в FastAPI.
        """
        return cls(
            name=name,
            project_id=project_id,
            description=description,
            date_from=date_from,
            date_to=date_to,
            contractor=contractor,
            type_task=type_task,
            status=status,
        )
