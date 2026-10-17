from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeacherCreate(BaseModel):
    employee_id: str
    user_id: int
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    joining_date: Optional[date] = None
    address: Optional[str] = None


class TeacherResponse(TeacherCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)