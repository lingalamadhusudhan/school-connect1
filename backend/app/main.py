from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db


app = FastAPI(
    title="School-Connect API",
    description="School-Connect School Management System API",
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


@app.get("/")
def home():
    return {
        "application": "School-Connect",
        "status": "running",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "school-connect-api",
    }


@app.get("/api/database/health")
def database_health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "PostgreSQL",
        "application": "School-Connect",
    }