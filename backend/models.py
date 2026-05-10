from sqlalchemy import Column, Integer, String, Date
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(20))


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(255))
    status = Column(String(20), default="TODO")
    due_date = Column(Date)
    project_id = Column(Integer)
    assigned_to = Column(Integer)