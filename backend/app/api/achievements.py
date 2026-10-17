from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.achievement import Achievement
from app.schemas.achievement import (
    AchievementCreate,
    AchievementResponse,
)


router = APIRouter(
    prefix="/api/achievements",
    tags=["Achievements"],
)


@router.post(
    "/",
    response_model=AchievementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_achievement(
    data: AchievementCreate,
    db: Session = Depends(get_db),
):
    achievement = Achievement(**data.model_dump())

    db.add(achievement)

    try:
        db.commit()
        db.refresh(achievement)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid student",
        )

    return achievement


@router.get(
    "/student/{student_id}",
    response_model=List[AchievementResponse],
)
def student_achievements(
    student_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Achievement)
        .filter(Achievement.student_id == student_id)
        .all()
    )