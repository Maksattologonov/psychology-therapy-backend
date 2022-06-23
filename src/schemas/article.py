from typing import Optional

from pydantic import BaseModel


class CreateArticleSchema(BaseModel):
    title: str
    description: str


class UpdateArticleSchema(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]


class GetArticleSchema(BaseModel):
    id: int
    title: str
    description: str
    image: Optional[str]

    class Config:
        orm_mode = True
