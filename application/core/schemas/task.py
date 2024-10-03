from datetime import date

from pydantic import BaseModel


class STask(BaseModel):
    name: str
    project_id: id
    description: str
    date_from: date
    date_to: date
    contractor: int
    status: str


class ReadTask(BaseModel):
    name: str
    project_name: str
    description: str
    date_from: str
    date_to: str
    contractor_email: str
    status: str

