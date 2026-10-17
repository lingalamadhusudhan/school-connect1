from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoticeCreate(BaseModel):
    title: str
    content: str
    audience: str
    created_by: int


class NoticeResponse(NoticeCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)