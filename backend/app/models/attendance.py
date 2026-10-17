from sqlalchemy import Column, Date, ForeignKey, Integer, String, UniqueConstraint

from app.db.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    attendance_date = Column(
        Date,
        nullable=False,
    )

    status = Column(
        String(20),
        nullable=False,
    )

    marked_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "attendance_date",
            name="uq_student_attendance_date",
        ),
    )