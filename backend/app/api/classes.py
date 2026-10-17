from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.school_class import SchoolClass
from app.schemas.school_class import ClassCreate, ClassResponse


router = APIRouter(
    prefix="/api/classes",
    tags=["Classes"],
)


@router.post(
    "/",
    response_model=ClassResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
):
    school_class = SchoolClass(**data.model_dump())

    db.add(school_class)

    try:
        db.commit()
        db.refresh(school_class)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid class teacher",
        )

    return school_class


@router.get(
    "/",
    response_model=List[ClassResponse],
)
def get_classes(
    db: Session = Depends(get_db),
):
    return db.query(SchoolClass).all()


@router.get(
    "/{class_id}",
    response_model=ClassResponse,
)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
):
    school_class = db.get(SchoolClass, class_id)

    if not school_class:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    return school_class