from typing import List

from pydantic import BaseModel, EmailStr

from application.core.models.user import PositionType


class SUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    position: str


class SUserLog(BaseModel):
    email: EmailStr
    password: str
