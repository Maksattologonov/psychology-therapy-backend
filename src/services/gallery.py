from typing import List

import sqlalchemy
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from common.exceptions import *

from core.database import Session
from models.accounts import User
from models.gallery import Gallery, GalleryImages
from schemas.accounts import UserSchema


class GalleryService:
    model = Gallery

    @classmethod
    def get(cls, db: Session, **filters):
        try:
            return db.query(cls.model).filter_by(**filters).first()
        except Exception:
            raise not_found_exception("Gallery")

    @classmethod
    async def filter(cls, db: Session, **filters):
        try:
            return db.query(cls.model).filter_by(**filters).all()
        except Exception:
            raise not_found_exception("Gallery")

    @classmethod
    async def delete(cls, db: Session, pk: int):
        try:
            if db.query(cls.model).filter_by(id=pk).delete():
                db.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content="Title successfully deleted")
        except Exception:
            raise not_found_exception("Gallery")

    @classmethod
    async def create_title(cls, db: Session, user: User, title: str, description: str):
        try:
            if title:
                record = cls.model(
                    title=title,
                    description=description
                )
                db.add(record)
                db.commit()
                return record
            raise not_validate from None
        except sqlalchemy.exc.IntegrityError:
            raise already_exist_exception("Title")

    @classmethod
    async def create(cls, db: Session, user: UserSchema, image_list: list, gallery_title_id: int):
        query = db.query(cls.model).filter_by(id=gallery_title_id).first()
        if image_list[0] and query:
            for img in image_list:
                url = f'images/gallery/{img.filename}'
                with open(url, 'wb') as file:
                    file.write(img.file.read())
                    file.close()
                    record = GalleryImages(
                        gallery_title_id=query.id,
                        images=url
                    )
                    db.add(record)
                    db.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content="Images successfully saved")
        raise not_found_exception("Gallery")

    @classmethod
    async def get_images(cls, db: Session, **filters):
        try:
            return db.query(GalleryImages).filter_by(**filters).all()
        except Exception:
            raise not_found_exception("Images")

