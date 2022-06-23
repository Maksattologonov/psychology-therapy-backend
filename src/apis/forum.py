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
from schemas.forum import CreateForumSchema, ForumSchema, GetForumSchema, DeleteForumSchema, ImagesForumSchema, \
    UpdateForumSchema, CreateForumDiscussion, UpdateForumDiscussion, CatalogSchema, CreateCatalogSchema
from services.accounts import get_current_user
from services.forum import ForumService, ForumDiscussionService, CatalogService

path = config("BASE_URL")
router = APIRouter(
    prefix='/catalog',
    include_in_schema=True,
    tags=['catalog']
)


@router.post('/create/', response_model=CatalogSchema, status_code=status.HTTP_201_CREATED,
             description="Create Catalog")
async def create_catalog(
        data: CreateCatalogSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: CatalogService = Depends(),
    ):
    return await service.create(data=data, user=user, db=db)


@router.delete('/delete', description="Delete catalog")
def delete_catalog(
        pk: int,
        user: User = Depends(get_current_user),
        service: CatalogService = Depends()
):
    return service.delete(id=pk)


@router.get('/get', description="Get catalog")
async def get_forum(
        service: CatalogService = Depends(),
        db: Session = Depends(get_session)
):
    return await service.filter(db=db)


@router.post('/create/forum', response_model=Union[ForumSchema, ImagesForumSchema],
             status_code=status.HTTP_201_CREATED,
             description="Creating forum")
async def create_forum(
        data: CreateForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends(),
        image: UploadFile or None = File(None)):
    return await service.create(catalog_id=data.catalog_id, title=data.title, description=data.description, user_id=user.id, image=image, db=db)


@router.get('/get/forum', description="Get all forum information")
async def get_forum(
        catalog_id: int,
        params: GetForumSchema = Depends(),
        service: ForumService = Depends(),
        db: Session = Depends(get_session)
):
    instance_slice = get_instance_slice(params.page, params.count)
    return await service.filter(db=db, params=params, catalog_id=catalog_id)


@router.get('/get-own/forum', description="Get all own forum information")
async def get_forum(
        params: GetForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends()
):
    return await service.filter(db=db, user_id=user.id, params=params)


@router.patch('/update/forum',
              description="Forum update")
async def update_forum(
        image: UploadFile or None = File(None),
        form: UpdateForumSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumService = Depends()
):
    return await service.update_forum(user_id=user.id, db=db, forum_id=form.id, catalog_id=form.catalog_id, title=form.title,
                                      description=form.description, image=image)


@router.delete('/delete/forum', description="Delete forum")
def delete_forum(
        pk: int,
        user: User = Depends(get_current_user),
        service: ForumService = Depends()
):
    return service.delete_forum(id=pk, user_id=user.id)


@router.get("/get-comment/forum")
async def get_comment(
        pk: int,
        db: Session = Depends(get_session),
        service: ForumDiscussionService = Depends()
):
    return service.filter(db=db, forum_id=pk)


@router.post("/create-comment/forum", response_model=CreateForumDiscussion, status_code=status.HTTP_201_CREATED,
             description="Create comment")
async def create_discussion(
        form: CreateForumDiscussion,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumDiscussionService = Depends()
):
    return await service.create(forum_id=form.forum_id, description=form.description, db=db, user=user)


@router.patch("/update-comment/forum")
def update_discussion(
        form: UpdateForumDiscussion,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ForumDiscussionService = Depends()
):
    return service.update(user_id=user.id, db=db, comment_id=form.comment_id, description=form.description)
