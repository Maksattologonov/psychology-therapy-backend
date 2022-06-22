import datetime
from typing import Optional

from pydantic import BaseModel

from models.appointments import TypeEnum, StatusEnum


class CreateAppointmentSchema(BaseModel):
    phone_number: str
    address: str
    status: StatusEnum
    type: TypeEnum
    date_time: str

    class Config:
        orm_mode = True


class UpdateAppointmentSchema(BaseModel):
    appointment_id: int
    status: StatusEnum


class GetAppointmentSchema(BaseModel):
    id: int
    date_time: str
    phone_number: str
    address: str
    status: StatusEnum
    type: TypeEnum

    class Config:
        orm_mode = True
