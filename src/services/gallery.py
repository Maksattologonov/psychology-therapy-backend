import sqlalchemy
from fastapi import HTTPException, status

from core.database import Session
from models.accounts import User
from models.gallery import Gallery


class GalleryService:
    model = Gallery

    @classmethod
    async def get(cls, db: Session, **filters):
        try:
            return db.query(cls.model).filter_by(**filters).first()
        except Exception:
            raise HTTPException(detail="Gallery not found")

    @classmethod
    async def filter(cls, db: Session, **filters):
        try:
            return db.query(cls.model).filter_by(**filters).all()
        except Exception:
            raise HTTPException(detail="Gallery not found")

    @classmethod
    async def create(cls, db: Session, user: User, title: str, description: str):
        try:
            if title:
                record = cls.model(
                    title=title,
                    description=description
                )
                db.add(record)
                db.commit()
                return record
            exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="could not validate credentials"
            )
            raise exception from None
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Title already exists"
            )

    @classmethod
    async def save_image(cls):
        return
