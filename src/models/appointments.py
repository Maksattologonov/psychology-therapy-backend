import enum

from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from core.database import Base


class StatusEnum(enum.IntEnum):
    NO_CHECKED = 1
    CHECKED = 2
    EXECUTED = 3


class TypeEnum(enum.IntEnum):
    SINGLE = 1
    MULTIPLE = 2


class Appointments(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    employee_id = Column(Integer, ForeignKey('users.id'))
    phone_number = Column(String(255))
    address = Column(String(255))
    status = Column(Integer)
    type = Column(Integer)
    date_time = Column(String(50), unique=True)
