from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.notice import Notice
from app.schemas.notice import NoticeCreate, NoticeResponse


router = APIRouter(
    prefix="/api/notices",
    tags=["Notices"],
)


@router.post(
    "/",
    response_model=NoticeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notice(
    data: NoticeCreate,
    db: Session = Depends(get_db),
):
    allowed = {
        "ALL",
        "TEACHERS",
        "PARENTS",
        "CLASS",
        "INDIVIDUAL",
    }

    audience = data.audience.upper()

    if audience not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Invalid notice audience",
        )

    payload = data.model_dump()
    payload["audience"] = audience

    notice = Notice(**payload)

    db.add(notice)

    try:
        db.commit()
        db.refresh(notice)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid notice creator",
        )

    return notice


@router.get(
    "/",
    response_model=List[NoticeResponse],
)
def get_notices(
    db: Session = Depends(get_db),
):
    return (
        db.query(Notice)
        .order_by(Notice.created_at.desc())
        .all()
    )