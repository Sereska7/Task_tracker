from datetime import date

from pydantic import BaseModel, EmailStr


class SBaseTask(BaseModel):
    name: str
    project_id: int
    description: str
    date_from: date
    date_to: date
    contractor: int
    type_task: str
    status: str


class SChangeTask(BaseModel):
    description: str
    date_from: date
    date_to: date
    contractor: int


class STask(BaseModel):
    name: str
    project_id: int
    description: str
    date_from: date
    date_to: date
    contractor: int


class SMyTask(BaseModel):
    name: str
    project_name: str
    description: str
    date_from: date
    date_to: date
    status: str


class ReadTask(BaseModel):
    name: str
    project_name: str
    description: str
    date_from: date
    date_to: date
    contractor_email: EmailStr
    type_task: str
    status: str
