from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False,
    )

    code = Column(
        String(30),
        unique=True,
        nullable=True,
    )

    class_id = Column(
        Integer,
        ForeignKey("classes.id"),
        nullable=False,
    )

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=True,
    )