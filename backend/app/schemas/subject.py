from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubjectCreate(BaseModel):
    name: str
    code: Optional[str] = None
    class_id: int
    teacher_id: Optional[int] = None


class SubjectResponse(SubjectCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)