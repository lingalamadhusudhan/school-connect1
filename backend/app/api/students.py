from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Students"],
)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Student)
        .filter(
            Student.admission_number
            == student_data.admission_number
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Admission number already exists",
        )

    student = Student(**student_data.model_dump())

    db.add(student)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid parent_id or class_id",
        )

    return student


@router.get(
    "/",
    response_model=List[StudentResponse],
)
def get_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return (
        db.query(Student)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    updates = student_data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid student update",
        )

    return student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.get(Student, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    db.delete(student)
    db.commit()

    return None