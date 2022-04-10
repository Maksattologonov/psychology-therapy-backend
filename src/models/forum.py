from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from core.database import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


forum = Forum.__table__


class ImagesForum(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    forum_id = Column(Integer, ForeignKey('forum.id', ondelete='CASCADE'))
    forum = relationship(Forum, lazy="joined", innerjoin=True, join_depth=3)
    images = Column(String(100))


forum_image = ImagesForum.__table__


class ForumDiscussion(Base):
    __tablename__ = 'forum_discussion'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    forum_id = Column(Integer, ForeignKey('forum.id'))
    title = Column(String(255), unique=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ImagesForumDiscussion(Base):
    __tablename__ = 'image_discussion'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    forum_id = Column(Integer, ForeignKey('forum_discussion.id', ondelete='CASCADE'))
    forum = relationship(ForumDiscussion, lazy="joined", innerjoin=True)
    images = Column(String(100))
