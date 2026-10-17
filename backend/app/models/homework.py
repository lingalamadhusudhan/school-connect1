from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.db.database import Base


class Homework(Base):
    __tablename__ = "homework"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    class_id = Column(
        Integer,
        ForeignKey("classes.id"),
        nullable=False,
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id"),
        nullable=False,
    )

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=False,
    )

    assigned_date = Column(
        Date,
        nullable=False,
    )

    due_date = Column(
        Date,
        nullable=True,
    )