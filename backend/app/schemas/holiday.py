from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HolidayCreate(BaseModel):
    name: str
    holiday_date: date
    description: Optional[str] = None


class HolidayResponse(HolidayCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)