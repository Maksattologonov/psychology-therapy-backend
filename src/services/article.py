from typing import Optional

import sqlalchemy
from fastapi import UploadFile, File, HTTPException, status

from core.database import Session
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
    async def filter(cls, db: Session, pk: Optional[int] = None):
        if pk:
            query = db.query(cls.model).filter_by(id=pk).all()
            if query:
                return query
        else:
            return db.query(cls.model).filter_by().all()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    @classmethod
    async def get(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).first()
        if query:
            return query
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

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
            raise HTTPException(detail="Article not found", status_code=status.HTTP_404_NOT_FOUND)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(detail="Title already exists", status_code=status.HTTP_409_CONFLICT)
        except Exception as ex:
            raise HTTPException(detail="Something went wrong", status_code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def delete_article(cls, db: Session, **filters):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
        if filters:
            if db.query(cls.model).filter_by(**filters).delete():
                db.commit()
                return HTTPException(
                    status_code=status.HTTP_202_ACCEPTED,
                    detail="Article successfully deleted"
                )
            raise exception
