import datetime

import sqlalchemy
from typing import Optional

from fastapi import UploadFile, File, HTTPException, status

from core.database import Session
from models.accounts import User
from models.appointments import Appointments


class AppointmentService:
    model = Appointments

    @classmethod
    async def create(cls, db: Session, description: str, user_id: User.id, date: datetime.datetime):
        try:
            if description and date:
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
                detail="There is already an entry for this date"
            )

    @classmethod
    async def get(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).all()
        if query:
            return query
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Appointment not found")

    @classmethod
    async def filter(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).all()
        if query:
            return query
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Appointment not found")

    @classmethod
    async def delete(cls, db: Session, pk: int, user_id: User.id):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
        if pk:
            if db.query(cls.model).filter_by(id=pk).delete():
                db.commit()
                return HTTPException(
                    status_code=status.HTTP_202_ACCEPTED,
                    detail="Appointment successfully deleted"
                )
            raise exception from None
