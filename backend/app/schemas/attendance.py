from datetime import date

from pydantic import BaseModel, ConfigDict


class AttendanceCreate(BaseModel):
    student_id: int
    attendance_date: date
    status: str
    marked_by: int


class AttendanceResponse(AttendanceCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)