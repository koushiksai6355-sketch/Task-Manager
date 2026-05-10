from pydantic import BaseModel

class SignupSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str


class LoginSchema(BaseModel):
    email: str
    password: str


class ProjectSchema(BaseModel):
    name: str
    description: str


class TaskSchema(BaseModel):
    title: str
    description: str
    due_date: str
    project_id: int
    assigned_to: int