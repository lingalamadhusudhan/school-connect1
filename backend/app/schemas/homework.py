from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HomeworkCreate(BaseModel):
    title: str
    description: Optional[str] = None
    class_id: int
    subject_id: int
    teacher_id: int
    assigned_date: date
    due_date: Optional[date] = None


class HomeworkResponse(HomeworkCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)