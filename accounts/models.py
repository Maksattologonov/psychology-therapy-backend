from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    anonymous_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_student = Column(Boolean, default=True)
    is_employee = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)