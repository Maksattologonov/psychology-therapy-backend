from typing import List

from fastapi import APIRouter, Depends, UploadFile, File

from core.database import get_session, Session
from models.accounts import User
from schemas.gallery import CreateGalleryTitleSchema, GalleryTitleSchema, CreateGallerySchema
from services.accounts import get_current_user
from services.gallery import GalleryService

router = APIRouter(
    prefix='/gallery',
    include_in_schema=True,
    tags=['gallery']
)


@router.post("/create/title", response_model=CreateGalleryTitleSchema)
async def create_gallery(form: CreateGalleryTitleSchema = Depends(),
                         user: User = Depends(get_current_user),
                         db: Session = Depends(get_session),
                         service: GalleryService = Depends()):
    return await service.create_title(db=db, title=form.title, description=form.description, user=user)


@router.get("/get/title")
async def get_gallery(
        db: Session = Depends(get_session),
        service: GalleryService = Depends()):
    return await service.filter(db=db)


@router.post("/create/")
async def create_gallery(form: CreateGallerySchema = Depends(),
                         image: List[UploadFile] = File(None),
                         user: User = Depends(get_current_user),
                         db: Session = Depends(get_session),
                         service: GalleryService = Depends()):
    return await service.create(db=db, user=user, image_list=image, gallery_title_id=form.gallery_title_id)


@router.get("/get-images/")
async def get_images(
        pk: int,
        db: Session = Depends(get_session),
        service: GalleryService = Depends()):
    return await service.get_images(db=db, gallery_title_id=pk)


@router.delete("/delete-title")
async def delete_title(
        pk: int,
        db: Session = Depends(get_session),
        service: GalleryService = Depends()):
    return await service.delete(db=db, pk=pk)
