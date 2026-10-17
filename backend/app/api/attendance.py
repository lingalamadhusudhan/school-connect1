from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.attendance import Attendance
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceResponse,
)


router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"],
)


@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def mark_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db),
):
    valid_statuses = {
        "PRESENT",
        "ABSENT",
        "LATE",
        "EXCUSED",
    }

    attendance_status = data.status.upper()

    if attendance_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid attendance status",
        )

    payload = data.model_dump()
    payload["status"] = attendance_status

    record = Attendance(**payload)

    db.add(record)

    try:
        db.commit()
        db.refresh(record)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid student/user or attendance "
                "already recorded for this date"
            ),
        )

    return record


@router.get(
    "/student/{student_id}",
    response_model=List[AttendanceResponse],
)
def student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(Attendance)
        .filter(Attendance.student_id == student_id)
        .order_by(Attendance.attendance_date.desc())
        .all()
    )