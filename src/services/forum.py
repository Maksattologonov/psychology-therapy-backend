import ast
import json
from typing import Optional

from fastapi import HTTPException, status, UploadFile
from core.database import Session
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
    def filter(cls, **filters):
        query = conn.query(cls.model).filter_by(**filters).all()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Forums not found'
            )
        return query

    @classmethod
    def get_with_image(cls):
        return

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
        record = cls.image_model(**filters)
        conn.add(record)
        conn.commit()
        return record

    @classmethod
    def create(cls, title: str, description: str, user_id: int, is_anonymous: bool = False):
        if title:
            record = cls.model(
                title=title,
                description=description,
                user_id=user_id,
                is_anonymous=is_anonymous
            )
            conn.add(record)
            conn.commit()
            return record
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="could not  validate credentials"
        )
        raise exception from None

    def save_image(self, image: UploadFile, forum_id: int) -> str:
        if image:
            url = f'images/forum/{image.filename}'
            forum = self.get(id=forum_id)
            with open(url, 'wb') as file:
                self.create_image(forum_id=forum.id, images=file.name)
                file.write(image.file.read())
                file.close()
            return url
