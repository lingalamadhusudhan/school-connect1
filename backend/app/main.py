from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="School-Connect API",
    description="Backend API for the School-Connect School Management System",
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
        "message": "Welcome to School-Connect API"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "school-connect-api"
    }