from sqlalchemy.orm import relationship

from core.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text


class Gallery(Base):

    __tablename__ = 'gallery'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(255))
    description = Column(Text)


class GalleryImages(Base):

    __tablename__ = 'gallery_image'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    gallery_title_id = Column(Integer, ForeignKey('gallery.id', ondelete='CASCADE'))
    gallery = relationship(Gallery, lazy="joined", innerjoin=True, join_depth=3)
    images = Column(String(200))
