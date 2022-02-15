import json
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Depends, Query
from starlette import status

from common.common import get_instance_slice
from models.accounts import User
from schemas.forum import CreateForumSchema, ForumSchema, GetForumSchema, DeleteForumSchema, ForumImage
from services.accounts import get_current_user
from services.forum import ForumService

router = APIRouter(
    prefix='/forum',
)


@router.post('/create-forum/', response_model=CreateForumSchema, status_code=status.HTTP_201_CREATED,
             description="Creating forum")
def create_forum(data: CreateForumSchema, user: User = Depends(get_current_user),
                 service: ForumService = Depends()):
    return service.create(title=data.title, description=data.description,
                          is_anonymous=data.is_anonymous, user_id=user.id)


@router.post('/upload-image/', description="Save image for forum")
def upload_image(forum_id: int, image: UploadFile = File(...), user: User = Depends(get_current_user),
                 service: ForumService = Depends()):
    return service.save_image(image=image, forum_id=forum_id)


@router.get('/get-forum/')
def get_forum(
        user_id: int = None,
        forum_id: int = None,
        page: int = 0,
        count: int = 5,
        service: ForumService = Depends()
):
    instance_slice = get_instance_slice(page, count)
    if user_id or forum_id:
        return service.get(is_anonymous=False, user_id=user_id, id=forum_id)
    return service.get(is_anonymous=False)[instance_slice]


@router.delete('/delete-forum')
def delete_forum(
        data: DeleteForumSchema = Depends(),
        user: User = Depends(get_current_user),
        service: ForumService = Depends()
):
    return service.delete_forum(id=data.id, user_id=user.id)
