from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey

from core.database import Base


class   User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    anonymous_name = Column(String(50), unique=True)
    hashed_password = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_student = Column(Boolean, default=True)
    is_employee = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class VerificationCode(Base):
    __tablename__ = "verification_code"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user = Column(String, ForeignKey("users.email"))
    code = Column(Integer)

