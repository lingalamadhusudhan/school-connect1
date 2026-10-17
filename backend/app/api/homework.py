from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.homework import Homework
from app.schemas.homework import HomeworkCreate, HomeworkResponse


router = APIRouter(
    prefix="/api/homework",
    tags=["Homework"],
)


@router.post(
    "/",
    response_model=HomeworkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_homework(
    data: HomeworkCreate,
    db: Session = Depends(get_db),
):
    if data.due_date and data.due_date < data.assigned_date:
        raise HTTPException(
            status_code=400,
            detail="Due date cannot be before assigned date",
        )

    homework = Homework(**data.model_dump())

    db.add(homework)

    try:
        db.commit()
        db.refresh(homework)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid class, subject or teacher",
        )

    return homework


@router.get(
    "/class/{class_id}",
    response_model=List[HomeworkResponse],
)
def class_homework(
    class_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Homework)
        .filter(Homework.class_id == class_id)
        .order_by(Homework.assigned_date.desc())
        .all()
    )