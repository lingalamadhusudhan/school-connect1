from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.exam import Exam
from app.schemas.exam import ExamCreate, ExamResponse


router = APIRouter(
    prefix="/api/exams",
    tags=["Exams"],
)


@router.post(
    "/",
    response_model=ExamResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exam(
    data: ExamCreate,
    db: Session = Depends(get_db),
):
    if data.maximum_marks <= 0:
        raise HTTPException(
            status_code=400,
            detail="Maximum marks must be greater than zero",
        )

    exam = Exam(**data.model_dump())

    db.add(exam)

    try:
        db.commit()
        db.refresh(exam)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid class or subject",
        )

    return exam


@router.get(
    "/",
    response_model=List[ExamResponse],
)
def get_exams(
    db: Session = Depends(get_db),
):
    return db.query(Exam).all()