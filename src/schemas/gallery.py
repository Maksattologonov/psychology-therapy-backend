from typing import List

from fastapi import UploadFile, File
from pydantic import BaseModel


class CreateGalleryTitleSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class GalleryTitleSchema(BaseModel):
    class Config:
        orm_mode = True


class CreateGallerySchema(BaseModel):
    gallery_title_id: int

    class Config:
        orm_mode = True

