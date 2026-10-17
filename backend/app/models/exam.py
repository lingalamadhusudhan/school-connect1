from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String

from app.db.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
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

    exam_date = Column(
        Date,
        nullable=False,
    )

    maximum_marks = Column(
        Numeric(6, 2),
        nullable=False,
    )