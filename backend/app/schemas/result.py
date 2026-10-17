from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResultCreate(BaseModel):
    exam_id: int
    student_id: int
    marks_obtained: Decimal
    grade: Optional[str] = None
    remarks: Optional[str] = None


class ResultResponse(ResultCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)