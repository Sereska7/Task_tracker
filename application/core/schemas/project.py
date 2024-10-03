from pydantic import BaseModel


class SProject(BaseModel):
    name: str
    description: str
