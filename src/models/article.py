from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from core.database import Base


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    image = Column(String(100))
