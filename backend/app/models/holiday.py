from sqlalchemy import Column, Date, Integer, String, Text

from app.db.database import Base


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
    )

    holiday_date = Column(
        Date,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )