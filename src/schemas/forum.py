from typing import List, Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class CreateForumSchema(BaseModel):
    title: str
    description: str
    is_anonymous: bool

    class Config:
        orm_mode = True


class ForumImage(BaseModel):
    image: str


class ForumSchema(BaseModel):
    id: int
    title: str
    description: str
    is_anonymous: bool

    class Config:
        orm_mode = True


class DeleteForumSchema(BaseModel):
    id: int


class GetForumSchema(BaseModel):
    page: int = 0
    count: int = 5
