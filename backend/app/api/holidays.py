from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.holiday import Holiday
from app.schemas.holiday import HolidayCreate, HolidayResponse


router = APIRouter(
    prefix="/api/holidays",
    tags=["Holidays"],
)


@router.post(
    "/",
    response_model=HolidayResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_holiday(
    data: HolidayCreate,
    db: Session = Depends(get_db),
):
    holiday = Holiday(**data.model_dump())

    db.add(holiday)
    db.commit()
    db.refresh(holiday)

    return holiday


@router.get(
    "/",
    response_model=List[HolidayResponse],
)
def get_holidays(
    db: Session = Depends(get_db),
):
    return (
        db.query(Holiday)
        .order_by(Holiday.holiday_date)
        .all()
    )