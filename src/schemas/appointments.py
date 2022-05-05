import datetime

from pydantic import BaseModel

from schemas.accounts import UserSchema


class CreateAppointmentSchema(BaseModel):
    description: str
    date: datetime.datetime


class GetAppointmentSchema(BaseModel):
    id: int
    description: str
    date: datetime.datetime

    class Config:
        orm_mode = True
