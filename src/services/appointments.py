import datetime

import sqlalchemy
from typing import Optional

from fastapi import UploadFile, File, HTTPException, status

from core.database import Session
from models.appointments import Appointments


class AppointmentService:
    model = Appointments

    @classmethod
    async def create(cls, db: Session, description: str, user_id: int, date: datetime.datetime):
        try:
            record = cls.model(
                description=description,
                user_id=user_id,
                date=date
            )
            db.add(record)
            db.commit()
            return record
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Title already exists"
            )

    @classmethod
    async def get(cls, db: Session, **filters):
        return db.query(cls.model).filter_by(**filters).first()

    @classmethod
    async def filter(cls, db: Session, **filters):
        return db.query(cls.model).filter_by(**filters).all()
