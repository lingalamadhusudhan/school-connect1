from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api import (
    achievements,
    attendance,
    classes,
    exams,
    holidays,
    homework,
    notices,
    results,
    students,
    subjects,
    teachers,
)
from app.db.database import get_db


app = FastAPI(
    title="School-Connect API",
    description="School-Connect School Management System",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(classes.router)
app.include_router(subjects.router)
app.include_router(attendance.router)
app.include_router(homework.router)
app.include_router(notices.router)
app.include_router(exams.router)
app.include_router(results.router)
app.include_router(achievements.router)
app.include_router(holidays.router)


@app.get("/", tags=["System"])
def home():
    return {
        "application": "School-Connect",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/api/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "service": "school-connect-api",
    }


@app.get(
    "/api/database/health",
    tags=["System"],
)
def database_health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "PostgreSQL",
    }