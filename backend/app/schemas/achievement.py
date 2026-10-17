from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AchievementCreate(BaseModel):
    student_id: int
    title: str
    description: Optional[str] = None
    achievement_date: Optional[date] = None
    category: Optional[str] = None


class AchievementResponse(AchievementCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)