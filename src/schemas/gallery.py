from pydantic import BaseModel


class CreateGalleryTitleSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class GalleryTitleSchema(BaseModel):
    class Config:
        orm_mode = True
