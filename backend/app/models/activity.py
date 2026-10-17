from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.db.database import Base


class StudentActivity(Base):
    __tablename__ = "student_activities"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    activity_name = Column(
        String(150),
        nullable=False,
    )

    activity_type = Column(
        String(50),
        nullable=True,
    )

    activity_date = Column(
        Date,
        nullable=True,
    )

    remarks = Column(
        Text,
        nullable=True,
    )