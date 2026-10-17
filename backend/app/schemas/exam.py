from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ExamCreate(BaseModel):
    name: str
    class_id: int
    subject_id: int
    exam_date: date
    maximum_marks: Decimal


class ExamResponse(ExamCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)