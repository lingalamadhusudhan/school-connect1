from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(50),
        nullable=False,
    )

    section = Column(
        String(20),
        nullable=False,
    )

    academic_year = Column(
        String(20),
        nullable=False,
    )

    class_teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=True,
    )