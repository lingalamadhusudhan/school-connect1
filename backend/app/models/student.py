from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    admission_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name = Column(
        String(80),
        nullable=False,
    )

    last_name = Column(
        String(80),
        nullable=True,
    )

    date_of_birth = Column(
        Date,
        nullable=True,
    )

    gender = Column(
        String(20),
        nullable=True,
    )

    blood_group = Column(
        String(10),
        nullable=True,
    )

    address = Column(
        String(500),
        nullable=True,
    )

    parent_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    class_id = Column(
        Integer,
        ForeignKey("classes.id"),
        nullable=True,
    )