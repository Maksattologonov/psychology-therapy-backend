import ast
import json
import sys
from typing import Optional, List

import sqlalchemy
from fastapi import HTTPException, status, UploadFile, File, Depends
from sqlalchemy.orm import lazyload, joinedload

from core.database import Session, get_session
from models.accounts import User
from models.forum import Forum, ImagesForum

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
            for i in range(len(query)):
                instance = cls.get_image(db=db, forum_id=query[i].id)
                request.append({"id": query[i].id, "title": query[i].title, "description": query[i].description,
                                "updated_at": query[i].updated_at, "created_at": query[i].created_at,
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
    def create_image(cls, **filters):
        try:
            record = cls.image_model(**filters)
            conn.add(record)
            conn.commit()
            conn.refresh(record)
            return record
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad credentials"
            )
        finally:
            conn.close()

    @classmethod
    def create(cls, title: str, description: str, user_id: int,
               image: Optional[List[UploadFile]] = File(None)):
        try:
            if title:
                record = cls.model(
                    title=title,
                    description=description,
                    user_id=user_id,
                )
                conn.add(record)
                conn.commit()
                cls.save_image(image=image, forum=title)
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
    async def save_image(cls, forum: str, image: Optional[List[UploadFile]] = File(None)) -> str:
        if image:
            for img in image:
                url = f'images/forum/{img.filename}'
                with open(url, 'wb') as file:
                    file.write(img.file.read())
                    query = cls.get(title=forum)
                    record = await cls.create_image(images=url, forum_id=query.id)
                    file.close()
            return record
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image saving error")

    @classmethod
    def update_forum(cls, forum_id: int, user_id: int, db: Session, title: str, description: str,
                     images: Optional[List[UploadFile]] = File(None)):
        query = db.query(Forum).filter_by(id=forum_id, user_id=user_id)
        if title:
            query.update({"title": title})
            db.commit()
        if description:
            query.update({"description": description})
            db.commit()
        if images:
            cls.save_image(image=images, forum=title)
        return query
        # except Exception as ex:
        #     raise HTTPException(detail="Something went wrong", status_code=status.HTTP_400_BAD_REQUEST)
