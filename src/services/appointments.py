import datetime
from enum import Enum

import sqlalchemy
from typing import Optional

from fastapi import UploadFile, File, HTTPException, status

from core.database import Session
from models.accounts import User
from models.appointments import Appointments


class AppointmentService:
    model = Appointments

    @classmethod
    async def create(cls, db: Session, phone_number: str, address: str, a_status: int,
                     user_id: User.id, typeof: int, date: datetime.datetime):
        try:
            if date:
                record = cls.model(
                    phone_number=phone_number,
                    address=address,
                    status=a_status,
                    type=typeof,
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
    async def update(cls, db: Session, appointment_id: int, a_status: int, user_id: User.id,):
        try:
            if user_id:
                query = db.query(cls.model).filter_by(id=appointment_id, user_id=user_id)
                if query.first():
                    if a_status:
                        query.update({"status": a_status})
                        db.commit()
                        db.commit()
                    return query.first()
            raise HTTPException(detail="Appointment not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            raise HTTPException(detail="Something went wrong", status_code=status.HTTP_400_BAD_REQUEST)

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
