from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectResponse


router = APIRouter(
    prefix="/api/subjects",
    tags=["Subjects"],
)


@router.post(
    "/",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
):
    subject = Subject(**data.model_dump())

    db.add(subject)

    try:
        db.commit()
        db.refresh(subject)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid class, teacher or subject code",
        )

    return subject


@router.get(
    "/",
    response_model=List[SubjectResponse],
)
def get_subjects(
    db: Session = Depends(get_db),
):
    return db.query(Subject).all()