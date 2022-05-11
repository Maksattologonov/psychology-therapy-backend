import json
import os
import sys
from typing import List, Optional, Union

from decouple import config
from fastapi import APIRouter, File, UploadFile, Depends, Query
from starlette import status
from starlette.responses import FileResponse

from common.common import get_instance_slice
from core.database import Session, get_session
from models.accounts import User
from models.forum import Forum, ImagesForum
from schemas.forum import CreateForumSchema, ForumSchema, GetForumSchema, DeleteForumSchema, ImagesForumSchema, \
    UpdateForumSchema, CreateForumDiscussion, UpdateForumDiscussion
from services.accounts import get_current_user
from services.forum import ForumService, ForumDiscussionService

path = config("BASE_URL")
router = APIRouter(
    prefix='/forum',
    include_in_schema=True,
    tags=['forum']
)


@router.post('/create/', response_model=Union[ForumSchema, ImagesForumSchema],
             status_code=status.HTTP_201_CREATED,
             description="Creating forum")
async def create_forum(
        data: CreateForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends(),
        image: UploadFile or None = File(None)):
    return await service.create(title=data.title, description=data.description, user_id=user.id, image=image, db=db)


@router.get('/get', description="Get all forum information")
async def get_forum(
        params: GetForumSchema = Depends(),
        service: ForumService = Depends(),
        db: Session = Depends(get_session)
):
    instance_slice = get_instance_slice(params.page, params.count)
    return await service.filter(db=db)


@router.get('/get-own', description="Get all own forum information")
async def get_forum(
        params: GetForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends()
):
    instance_slice = get_instance_slice(params.page, params.count)
    return (await service.filter(db=db, user_id=user.id))[instance_slice]


@router.patch('/update',
              description="Forum update")
async def update_forum(
        image: UploadFile or None = File(None),
        form: UpdateForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends()
):
    return await service.update_forum(user_id=user.id, db=db, forum_id=form.id, title=form.title,
                                      description=form.description, image=image)


@router.delete('/delete', description="Delete forum")
def delete_forum(
        pk: int,
        user: User = Depends(get_current_user),
        service: ForumService = Depends()
):
    return service.delete_forum(id=pk, user_id=user.id)


@router.get("/get-comment")
async def get_comment(
        pk: int,
        db: Session = Depends(get_session),
        service: ForumDiscussionService = Depends()
):
    return service.filter(db=db, forum_id=pk)


@router.post("/create-comment", response_model=CreateForumDiscussion, status_code=status.HTTP_201_CREATED,
             description="Create comment")
async def create_discussion(
        form: CreateForumDiscussion,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumDiscussionService = Depends()
):
    return await service.create(forum_id=form.forum_id, description=form.description, db=db, user_id=user.id)


@router.patch("/update-comment")
def update_discussion(
        form: UpdateForumDiscussion,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumDiscussionService = Depends()
):
    return service.update(user_id=user.id, db=db, comment_id=form.comment_id, description=form.description)
