import datetime
import smtplib
import time
from email.message import EmailMessage
from enum import Enum

import sqlalchemy
from typing import Optional

from decouple import config
from fastapi import UploadFile, File, HTTPException, status
from jinja2 import Template

from common.message import raw_response
from core.database import Session
from models.accounts import User
from models.appointments import Appointments


class AppointmentService:
    model = Appointments

    @classmethod
    async def create(cls, db: Session, phone_number: str, address: str, a_status: int,
                     user_id: User.id, typeof: int, date: str):
        try:
            if date:
                record = cls.model(
                    phone_number=phone_number,
                    address=address,
                    status=a_status,
                    type=typeof,
                    user_id=user_id,
                    date_time=date
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
                user = db.query(User).filter_by(id=user_id).first()
                if query.first():
                    if a_status:
                        if a_status == 2:
                            bar = Template(raw_response)

                            template = bar.render(
                                messages={'name': f"{user.name + ' ' + user.last_name}",
                                          "time": str(query.first().date_time)})
                            message = EmailMessage()
                            message['Subject'] = f'Здравствуйте {user.name + " " + user.last_name}!'
                            message['From'] = config("MAIL_FROM")
                            message['To'] = user.email
                            message.add_alternative(template, subtype='html')
                            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            smtp.login(config("MAIL_FROM"), config("MAIL_PASSWORD"))
                            smtp.send_message(message)
                            smtp.quit()
                        query.update({"status": a_status})
                        db.commit()
                        db.commit()
                    return query.first()
            raise HTTPException(detail="Appointment not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            print(ex)
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
