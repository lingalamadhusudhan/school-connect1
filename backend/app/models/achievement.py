from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.db.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    achievement_date = Column(
        Date,
        nullable=True,
    )

    category = Column(
        String(100),
        nullable=True,
    )