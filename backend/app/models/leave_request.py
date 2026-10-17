from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from app.db.database import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)

    requester_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=True,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String(30),
        default="PENDING",
        nullable=False,
    )

    approved_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )