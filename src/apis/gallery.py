from fastapi import APIRouter, Depends

from core.database import get_session, Session
from models.accounts import User
from schemas.gallery import CreateGalleryTitleSchema, GalleryTitleSchema
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
    return await service.create(db=db, title=form.title, description=form.description, user=user)


@router.get("/get/title")
async def get_gallery(
                      db: Session = Depends(get_session),
                      service: GalleryService = Depends()):
    return await service.filter(db=db)