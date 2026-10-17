from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.database import Base


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    event_type = Column(
        String(50),
        nullable=True,
    )

    starts_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    ends_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )