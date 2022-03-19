from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean

from core.database import Base


class Forum(Base):
    __tablename__ = 'forum'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_anonymous = Column(Boolean, default=False)


class ImagesForum(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    forum_id = Column(Integer, ForeignKey('forum.id', ondelete='CASCADE'))
    images = Column(String(100))


class ForumDiscussion(Base):
    __tablename__ = 'forum_discussion'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    forum_id = Column(Integer, ForeignKey('forum.id'))
    title = Column(String(255))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    is_anonymous = Column(Boolean, default=False)


class ImagesForumDiscussion(Base):
    __tablename__ = 'images_forum_discussion'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    forum_id = Column(Integer, ForeignKey('forum_discussion.id', ondelete='CASCADE'))
    images = Column(String(100))
