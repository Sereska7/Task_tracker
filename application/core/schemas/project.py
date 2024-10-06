from fastapi import Form
from pydantic import BaseModel


class SProject(BaseModel):
    name: str
    description: str


class SProjectCreateForm(BaseModel):
    name: str
    description: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
    ):
        return cls(name=name, description=description)
