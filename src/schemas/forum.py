from typing import List, Optional, Type, Any

from fastapi import UploadFile, File
from pydantic import BaseModel
from core.database import Session


class CreateForumSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class ForumSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class ImagesForumSchema(BaseModel):
    id: int
    forum_id: int
    images: str

    class Config:
        orm_mode: True


class DeleteForumSchema(BaseModel):
    id: int


class GetForumSchema(BaseModel):
    count: int = 10
    page: int = 0


class UpdateForumSchema(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]


class CreateForumDiscussion(BaseModel):
    forum_id: int
    description: str

    class Config:
        orm_mode = True


class UpdateForumDiscussion(BaseModel):
    comment_id: int
    description: str

    class Config:
        orm_mode = True

