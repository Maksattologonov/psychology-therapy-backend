import json
import os
from typing import List, Optional

from decouple import config
from fastapi import APIRouter, File, UploadFile, Depends, Query
from starlette import status
from starlette.responses import FileResponse

from common.common import get_instance_slice
from core.database import Session, get_session
from models.accounts import User
from models.forum import Forum, ImagesForum
from schemas.forum import CreateForumSchema, ForumSchema, GetForumSchema, DeleteForumSchema, ImagesForumSchema, \
    UpdateForumSchema
from services.accounts import get_current_user
from services.forum import ForumService

path = config("BASE_URL")
router = APIRouter(
    prefix='/forum',
    include_in_schema=True,
    tags=['forum']
)


@router.post('/create-forum/', response_model=ForumSchema, status_code=status.HTTP_201_CREATED,
             description="Creating forum")
def create_forum(user: User = Depends(get_current_user),
                 service: ForumService = Depends(), data: CreateForumSchema = Depends(),
                 image: Optional[List[UploadFile]] = File(None)):
    return service.create(title=data.title, description=data.description, user_id=user.id, image=image)


@router.get('/get-forum/')
async def get_forum(
        params: GetForumSchema = Depends(),
        service: ForumService = Depends(),
        db: Session = Depends(get_session)
):
    instance_slice = get_instance_slice(params.page, params.count)
    return (await service.filter(db))[instance_slice]


@router.get('/get-my-forum/')
async def get_forum(
        params: GetForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends()
):
    instance_slice = get_instance_slice(params.page, params.count)
    return (await service.filter(db=db, user_id=user.id))[instance_slice]


@router.patch('/update-forum')
async def update_forum(
        images: Optional[List[UploadFile]] = File(None, description='Only fans'),
        form: UpdateForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends()
):
    return service.update_forum(user_id=user.id, db=db, forum_id=form.id, title=form.title,
                                description=form.description, images=images)


@router.delete('/delete-forum')
def delete_forum(
        pk: int,
        user: User = Depends(get_current_user),
        service: ForumService = Depends()
):
    return service.delete_forum(id=pk, user_id=user.id)
