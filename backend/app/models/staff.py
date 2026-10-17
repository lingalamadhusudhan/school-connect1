from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db.database import Base


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        String(50),
        unique=True,
        nullable=False,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    department = Column(
        String(100),
        nullable=True,
    )

    designation = Column(
        String(100),
        nullable=True,
    )

    joining_date = Column(
        Date,
        nullable=True,
    )