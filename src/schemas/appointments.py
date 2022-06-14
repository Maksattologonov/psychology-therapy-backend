import datetime
from typing import Optional

from pydantic import BaseModel

from models.appointments import MyEnum


class CreateAppointmentSchema(BaseModel):
    phone_number: str
    address: str
    description: Optional[str]
    status: MyEnum
    date: datetime.datetime

    class Config:
        orm_mode = True


class UpdateAppointmentSchema(BaseModel):
    appointment_id: int
    status: MyEnum


class GetAppointmentSchema(BaseModel):
    id: int
    description: str
    date: datetime.datetime

    class Config:
        orm_mode = True
