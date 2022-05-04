from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, status

from core.database import Session, get_session
from models.accounts import User
from schemas.appointments import CreateAppointmentSchema
from services.accounts import get_current_user
from services.appointments import AppointmentService

router = APIRouter(
    prefix='/appointment',
    include_in_schema=True,
    tags=['appointment']
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_appointment(
        form: CreateAppointmentSchema = Depends(),
        db: Session = Depends(get_session),
        user: User = Depends(get_current_user),
        service: AppointmentService = Depends()
):
    return await service.create(db=db, date=form.date, description=form.description, user_id=user.id)


@router.get("/get")
async def get_appointment(
        db: Session = Depends(get_session),
        service: AppointmentService = Depends()
):
    return await service.filter(db=db)


@router.get("/get-own")
async def get_appointment(
        db: Session = Depends(get_session),
        user: User = Depends(get_current_user),
        service: AppointmentService = Depends()
):
    return await service.get(db=db, user_id=user.id)


@router.delete("/delete")
async def delete(
        pk: int,
        service: AppointmentService = Depends(),
        db: Session = Depends(get_session),
        user: User = Depends(get_current_user)
):
    return await service.delete(db=db, user_id=user.id, pk=pk)
