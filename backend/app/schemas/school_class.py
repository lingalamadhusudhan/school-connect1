from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClassCreate(BaseModel):
    name: str
    section: str
    academic_year: str
    class_teacher_id: Optional[int] = None


class ClassResponse(ClassCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)