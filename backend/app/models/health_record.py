from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.db.database import Base


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
    )

    record_date = Column(
        Date,
        nullable=False,
    )

    blood_group = Column(
        String(10),
        nullable=True,
    )

    height_cm = Column(
        String(20),
        nullable=True,
    )

    weight_kg = Column(
        String(20),
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    recorded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )