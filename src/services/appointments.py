import datetime
import smtplib
import time
from email.message import EmailMessage
from enum import Enum

import sqlalchemy
from typing import Optional
from common.exceptions import *

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
    async def create(cls, db: Session, employee_id: int, phone_number: str, address: str, a_status: int,
                     user_id: User.id, typeof: int, date: str):
        try:
            employee = db.query(User).filter_by(id=employee_id, is_employee=True).first()
            if employee:
                record = cls.model(
                    phone_number=phone_number,
                    address=address,
                    employee_id=employee_id,
                    status=a_status,
                    type=typeof,
                    user_id=user_id,
                    date_time=date
                )
                db.add(record)
                db.commit()
                return record
            else:
                raise not_found_exception("Employee")
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
        except Exception as ex:
            raise not_found_exception("User")

    @classmethod
    async def get(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).all()
        if query:
            return query
        raise not_found_exception("Appointment")

    @classmethod
    async def filter(cls, db: Session, **filters):
        query = db.query(cls.model).filter_by(**filters).all()
        if query:
            return query
        raise not_found_exception("Appointment")

    @classmethod
    async def delete(cls, db: Session, pk: int, user_id: User.id):
        if pk:
            if db.query(cls.model).filter_by(id=pk).delete():
                db.commit()
                return HTTPException(
                    status_code=status.HTTP_202_ACCEPTED,
                    detail="Appointment successfully deleted"
                )
            raise not_found_exception("Appointment") from None
