from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from database import Base, engine, SessionLocal
from models import User, Project, Task
from schemas import *
from auth import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- SIGNUP ----------------
@app.post("/signup")
def signup(user: SignupSchema, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role.lower()
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({"id": user.id, "role": user.role})

    return {"token": token, "role": user.role}

# ---------------- PROJECTS ----------------
@app.post("/projects")
def create_project(
    project: ProjectSchema,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    admin_required(user)

    new_project = Project(**project.dict())
    db.add(new_project)
    db.commit()

    return {"message": "Project created"}

@app.get("/projects")
def get_projects(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Project).all()

# ---------------- TASKS ----------------
@app.post("/tasks")
def create_task(
    task: TaskSchema,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()

    return {"message": "Task created"}

@app.get("/tasks")
def get_tasks(user=Depends(get_current_user), db: Session = Depends(get_db)):

    if user["role"] == "admin":
        return db.query(Task).all()

    return db.query(Task).filter(Task.assigned_to == user["id"]).all()

# ---------------- DASHBOARD ----------------
@app.get("/dashboard")
def dashboard(user=Depends(get_current_user), db: Session = Depends(get_db)):

    tasks = db.query(Task).all()

    return {
        "total": len(tasks),
        "completed": len([t for t in tasks if t.status == "DONE"]),
        "pending": len([t for t in tasks if t.status != "DONE"]),
        "overdue": len([
            t for t in tasks
            if str(t.due_date) < str(datetime.today().date())
        ])
    }