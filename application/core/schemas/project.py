from fastapi import Form
from pydantic import BaseModel


# Модель данных для представления проекта
class SProject(BaseModel):
    """
    Класс SProject используется для отображения данных проекта.
    """
    name: str  # Имя проекта
    description: str  # Описание проекта


# Модель формы для создания проекта
class SProjectCreateForm(BaseModel):
    """
    Класс SProjectCreateForm используется для валидации данных формы при создании нового проекта.
    """
    name: str  # Имя проекта
    description: str  # Описание проекта

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),  # Поле для имени проекта, обязательное
        description: str = Form(...),  # Поле для описания проекта, обязательное
    ):
        """
        Метод класса для создания объекта формы, используемого в маршрутах FastAPI.
        """
        return cls(name=name, description=description)
