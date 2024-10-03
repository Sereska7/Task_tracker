from datetime import date

from pydantic import BaseModel, EmailStr


class STask(BaseModel):
    name: str
    project_id: int
    description: str
    date_from: date
    date_to: date
    contractor: int


class ReadTask(BaseModel):
    name: str
    project_name: str
    description: str
    date_from: date
    date_to: date
    contractor_email: EmailStr
    type_task: str
    status: str

