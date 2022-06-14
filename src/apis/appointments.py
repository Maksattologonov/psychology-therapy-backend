from typing import Optional, Union

from fastapi import APIRouter, Depends, UploadFile, File, status

from core.database import Session, get_session
from models.accounts import User
from schemas.appointments import CreateAppointmentSchema, GetAppointmentSchema, UpdateAppointmentSchema
from services.accounts import get_current_user
from services.appointments import AppointmentService

router = APIRouter(
    prefix='/appointment',
    include_in_schema=True,
    tags=['appointment']
)


@router.post("/create", response_model=GetAppointmentSchema, status_code=status.HTTP_201_CREATED)
async def create_appointment(
        form: CreateAppointmentSchema = Depends(),
        db: Session = Depends(get_session),
        user: User = Depends(get_current_user),
        service: AppointmentService = Depends()
):
    return await service.create(db=db, phone_number=form.phone_number, address=form.address, a_status=form.status.value,
                                date=form.date, description=form.description, user_id=user.id)


@router.put("/update", response_model=GetAppointmentSchema, status_code=status.HTTP_201_CREATED)
async def update_appointment(
        form: UpdateAppointmentSchema = Depends(),
        db: Session = Depends(get_session),
        user: User = Depends(get_current_user),
        service: AppointmentService = Depends()
):
    return await service.update(db=db, a_status=form.status.value, appointment_id=form.appointment_id, user_id=user.id)


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
