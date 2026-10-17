from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, UniqueConstraint

from app.db.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)

    exam_id = Column(
        Integer,
        ForeignKey("exams.id"),
        nullable=False,
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    marks_obtained = Column(
        Numeric(6, 2),
        nullable=False,
    )

    grade = Column(
        String(10),
        nullable=True,
    )

    remarks = Column(
        String(500),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "exam_id",
            "student_id",
            name="uq_exam_student_result",
        ),
    )