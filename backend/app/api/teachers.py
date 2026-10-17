from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherResponse


router = APIRouter(
    prefix="/api/teachers",
    tags=["Teachers"],
)


@router.post(
    "/",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_teacher(
    data: TeacherCreate,
    db: Session = Depends(get_db),
):
    teacher = Teacher(**data.model_dump())

    db.add(teacher)

    try:
        db.commit()
        db.refresh(teacher)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=(
                "Employee ID already exists or "
                "user_id is invalid"
            ),
        )

    return teacher


@router.get(
    "/",
    response_model=List[TeacherResponse],
)
def get_teachers(
    db: Session = Depends(get_db),
):
    return db.query(Teacher).all()


@router.get(
    "/{teacher_id}",
    response_model=TeacherResponse,
)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
):
    teacher = db.get(Teacher, teacher_id)

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    return teacher