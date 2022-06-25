from typing import Optional

import sqlalchemy
from fastapi import UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from common.exceptions import *


from core.database import Session
from models.accounts import User
from models.article import Article


class ArticleService:
    model = Article

    @classmethod
    async def create(cls, db: Session, title: str, description: str, user_id: int,
                     image: Optional[UploadFile] = File(None)):
        try:
            if image:
                url = f'images/forum/{image.filename}'
                record = cls.model(
                    title=title,
                    description=description,
                    user_id=user_id,
                    image=url
                )
                db.add(record)
                with open(url, 'wb') as file:
                    file.write(image.file.read())
                    file.close()
                db.commit()
                return record
            elif title and not image:
                record = cls.model(
                    title=title,
                    description=description,
                    user_id=user_id,
                )
                db.add(record)
                db.commit()
                return record
            raise not_validate from None
        except sqlalchemy.exc.IntegrityError:
            raise already_exist_exception("Title")

    @classmethod
    async def filter(cls, db: Session, pk: Optional[int] = None):
        if pk:
            query = db.query(cls.model).filter_by(id=pk).all()
            if query:
                return query
        else:
            return db.query(cls.model).filter_by().all()
        raise not_found_exception("Article")

    @classmethod
    async def get(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).first()
        if query:
            return query
        raise not_found_exception("Article")

    @classmethod
    async def update_article(cls, user_id: int, db: Session, article_id: int, title: str,
                             description: str, image: Optional[UploadFile] = File(None)):
        try:
            if user_id:
                query = db.query(cls.model).filter_by(id=article_id, user_id=user_id)
                if query:
                    if title:
                        query.update({"title": title})
                        db.commit()
                    if description:
                        query.update({"description": description})
                        db.commit()
                    if image:
                        url = f'images/forum/{image.filename}'
                        with open(url, 'wb') as file:
                            file.write(image.file.read())
                            file.close()
                        query.update({"image": url})
                        db.commit()
                    return query.first()
            raise not_found_exception("Article")
        except sqlalchemy.exc.IntegrityError:
            raise already_exist_exception("Title")
        except Exception as ex:
            raise HTTPException(detail="Something went wrong", status_code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete_article(cls, db: Session, pk: int, user: User):
        if user.is_superuser:
            if db.query(cls.model).filter_by(id=pk).delete():
                db.commit()
                return JSONResponse(
                    status_code=status.HTTP_202_ACCEPTED,
                    content="Article successfully deleted"
                )
        raise permission_exception
