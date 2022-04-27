from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey

from core.database import Base


class Appointments(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(Text)
    date = Column(DateTime(timezone=True))
