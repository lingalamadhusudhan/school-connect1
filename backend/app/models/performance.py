from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text

from app.db.database import Base


class StudentPerformance(Base):
    __tablename__ = "student_performance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    period_type = Column(
        String(20),
        nullable=False,
    )

    period = Column(
        String(30),
        nullable=False,
    )

    academic_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    attendance_score = Column(
        Numeric(5, 2),
        nullable=True,
    )

    remarks = Column(
        Text,
        nullable=True,
    )