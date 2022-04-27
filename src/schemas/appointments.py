import datetime

from pydantic import BaseModel


class CreateAppointmentSchema(BaseModel):
    description: str
    date: datetime.datetime
