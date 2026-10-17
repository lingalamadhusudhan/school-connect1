from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    admission_number: str
    first_name: str
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    parent_id: Optional[int] = None
    class_id: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    parent_id: Optional[int] = None
    class_id: Optional[int] = None


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)