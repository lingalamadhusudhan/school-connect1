from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    qualification = Column(
        String(150),
        nullable=True,
    )

    specialization = Column(
        String(150),
        nullable=True,
    )

    joining_date = Column(
        Date,
        nullable=True,
    )

    address = Column(
        String(500),
        nullable=True,
    )