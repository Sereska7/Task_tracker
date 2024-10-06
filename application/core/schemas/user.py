from pydantic import BaseModel, EmailStr
from fastapi import Form

from application.core.models.user import PositionType


class SUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    position: PositionType


class SUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    position: str


class UserRead:
    id: int
    name: str
    email: EmailStr
    position: str


class SUserLog(BaseModel):
    email: EmailStr
    password: str


class SUserLogForm(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(email=email, password=password)


class SUserCreateForm(BaseModel):
    name: str
    email: str
    password: str
    position: PositionType

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        position: PositionType = Form(...)
    ):
        return cls(name=name, email=email, password=password, position=position)
