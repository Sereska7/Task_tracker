from datetime import date

from fastapi import Form
from pydantic import BaseModel, EmailStr

from application.core.models.task import TypeTask, TaskStatus


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
    contractor_email: str
    date_from: date
    date_to: date
    status: str


class ReadTask(BaseModel):
    name: str
    project_name: str
    description: str
    date_from: date
    date_to: date
    type_task: str
    status: str


class STaskCreateForm(BaseModel):
    name: str
    project_id: int
    description: str
    date_from: date
    date_to: date
    contractor: int
    type_task: TypeTask
    status: TaskStatus

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        project_id: int = Form(...),
        description: str = Form(...),
        date_from: date = Form(...),
        date_to: date = Form(...),
        contractor: int = Form(...),
        type_task: TypeTask = Form(...),
        status: TaskStatus = Form(...),
    ):
        return cls(name=name, project_id=project_id, description=description, date_from=date_from, date_to=date_to,
                   contractor=contractor, type_task=type_task, status=status)
