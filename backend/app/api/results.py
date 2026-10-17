from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.exam import Exam
from app.models.result import Result
from app.schemas.result import ResultCreate, ResultResponse


router = APIRouter(
    prefix="/api/results",
    tags=["Results"],
)


@router.post(
    "/",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_result(
    data: ResultCreate,
    db: Session = Depends(get_db),
):
    exam = db.get(Exam, data.exam_id)

    if not exam:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    if data.marks_obtained < 0:
        raise HTTPException(
            status_code=400,
            detail="Marks cannot be negative",
        )

    if data.marks_obtained > exam.maximum_marks:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Marks cannot exceed "
                f"{exam.maximum_marks}"
            ),
        )

    result = Result(**data.model_dump())

    db.add(result)

    try:
        db.commit()
        db.refresh(result)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid student or result already exists "
                "for this exam"
            ),
        )

    return result


@router.get(
    "/student/{student_id}",
    response_model=List[ResultResponse],
)
def student_results(
    student_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Result)
        .filter(Result.student_id == student_id)
        .all()
    )