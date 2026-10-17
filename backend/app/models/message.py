from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.sql import func

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    sender_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    receiver_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )