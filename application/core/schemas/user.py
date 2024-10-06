from pydantic import BaseModel, EmailStr
from fastapi import Form

from application.core.models.user import PositionType


# Модель для создания нового пользователя
class SUserCreate(BaseModel):
    """
    Класс SUserCreate используется для представления данных при создании нового пользователя.
    """
    name: str  # Имя пользователя
    email: EmailStr  # Email пользователя, проверяется как валидный адрес
    password: str  # Пароль пользователя
    position: PositionType  # Должность пользователя (директор, менеджер и т.д.)


# Модель для отображения данных существующего пользователя
class SUser(BaseModel):
    """
    Класс SUser представляет данные пользователя, которые возвращаются после запросов.
    """
    id: int  # Идентификатор пользователя
    name: str  # Имя пользователя
    email: EmailStr  # Email пользователя
    position: str  # Должность пользователя


# Модель для авторизации пользователя (логин)
class SUserLog(BaseModel):
    """
    Класс SUserLog используется для авторизации пользователя.
    """
    email: EmailStr  # Email пользователя
    password: str  # Пароль пользователя


# Модель формы для авторизации пользователя (используется в FastAPI)
class SUserLogForm(BaseModel):
    """
    Класс SUserLogForm используется для создания формы входа.
    """
    email: str  # Email пользователя
    password: str  # Пароль пользователя

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...)):
        """
        Метод для создания формы авторизации в FastAPI.
        """
        return cls(email=email, password=password)


# Модель формы для регистрации нового пользователя
class SUserCreateForm(BaseModel):
    """
    Класс SUserCreateForm используется для создания формы регистрации.
    """
    name: str  # Имя пользователя
    email: str  # Email пользователя
    password: str  # Пароль пользователя
    position: PositionType  # Должность пользователя (директор, менеджер и т.д.)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),  # Поле формы для имени пользователя
        email: str = Form(...),  # Поле формы для email пользователя
        password: str = Form(...),  # Поле формы для пароля
        position: PositionType = Form(...),  # Поле формы для выбора должности
    ):
        """
        Метод для создания формы регистрации нового пользователя в FastAPI.
        """
        return cls(name=name, email=email, password=password, position=position)
