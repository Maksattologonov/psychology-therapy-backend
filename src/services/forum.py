import ast
import json
import sys
from typing import Optional, List

import sqlalchemy
from fastapi import HTTPException, status, UploadFile, File, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload, aliased

from core.database import Session, get_session
from models.accounts import User
from models.forum import Forum, ImagesForum, forum

conn = Session()


class ForumService:
    model = Forum
    image_model = ImagesForum

    @classmethod
    def get(cls, **filters):
        query = conn.query(cls.model).filter_by(**filters).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Forum not found'
            )
        return query

    @classmethod
    async def filter(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).all()
        request = []
        if query:
            for i in query:
                instance = cls.get_image(db=db, forum_id=i.id)
                request.append({"id": i.id, "title": i.title, "description": i.description,
                                "updated_at": i.updated_at, "created_at": i.created_at,
                                "images": instance})
            return request
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Forums not found'
        )

    @classmethod
    def get_image(cls, db: Session, **filters):
        return db.query(cls.image_model.id, cls.image_model.images).filter_by(**filters).all()

    @classmethod
    def delete_forum(cls, **filters):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )
        if filters:
            if conn.query(cls.model).filter_by(**filters).delete():
                conn.commit()
                return HTTPException(
                    status_code=status.HTTP_202_ACCEPTED,
                    detail="forum successfully deleted"
                )
            raise exception from None
            # except Exception as ex:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail='Something went wrong'
            #     ) from None

    @classmethod
    async def create_image(cls, **filters):
        try:
            record = cls.image_model(**filters)
            conn.add(record)
            conn.commit()
            return record
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad credentials"
            )

    @classmethod
    async def create(cls, db: Session, title: str, description: str, user_id: int,
                     image: Optional[UploadFile] = File(None)):
        try:
            if title:
                record = cls.model(
                    title=title,
                    description=description,
                    user_id=user_id,
                )
                db.add(record)
                db.commit()
                if image:
                    await cls.save_image(image=image, title=title)
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
    async def save_image(cls, title: str, image: Optional[UploadFile] = File(None)):
        if image:
            # for img in image:
            url = f'images/forum/{image.filename}'
            with open(url, 'wb') as file:
                file.write(image.file.read())
                query = cls.get(title=title)
                file.close()
                await cls.create_image(images=url, forum_id=query.id)
            return query
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image saving error")

    @classmethod
    async def update_forum(cls, db: Session, forum_id: int, user_id: int, title: str, description: str,
                           image: Optional[UploadFile] = File(None)):
        try:
            query = db.query(Forum).filter_by(id=forum_id, user_id=user_id)
            if query:
                if title:
                    query.update({"title": title})
                    db.commit()
                if description:
                    query.update({"description": description})
                    db.commit()
                if image:
                    record = db.query(cls.image_model).filter_by(forum_id=query.first().id)
                    url = f'images/forum/{image.filename}'
                    with open(url, 'wb') as file:
                        file.write(image.file.read())
                        query = cls.get(title=title)
                        file.close()
                    record.update({'images': url})
                    db.commit()
                return query
            raise HTTPException(detail="Forum not found", status_code=status.HTTP_404_NOT_FOUND)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(detail="Title already exists", status_code=status.HTTP_409_CONFLICT)
        except Exception as ex:
            raise HTTPException(detail="Something went wrong", status_code=status.HTTP_400_BAD_REQUEST)
