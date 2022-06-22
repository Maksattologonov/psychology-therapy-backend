from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, status

from core.database import Session, get_session
from models.accounts import User
from schemas.article import CreateArticleSchema, UpdateArticleSchema, GetArticleSchema
from services.accounts import get_current_user
from services.article import ArticleService

router = APIRouter(
    prefix='/article',
    include_in_schema=True,
    tags=['article']
)


@router.post("/create", response_model=GetArticleSchema, status_code=status.HTTP_201_CREATED)
async def create_article(
        form: CreateArticleSchema = Depends(),
        db: Session = Depends(get_session),
        image: UploadFile or None = File(None),
        user: User = Depends(get_current_user),
        service: ArticleService = Depends()
):
    return await service.create(db=db, title=form.title, description=form.description, user_id=user.id, image=image)


@router.get('/get', description="Get article information")
async def get_forum(
        pk: Optional[int] = None,
        service: ArticleService = Depends(),
        db: Session = Depends(get_session)
):
    return await service.filter(db=db, pk=pk)


@router.patch('/update', response_model=GetArticleSchema, description="Article update")
async def update_forum(
        image: UploadFile or None = File(None),
        form: UpdateArticleSchema = Depends(),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ArticleService = Depends()
):
    return await service.update_article(user_id=user.id, db=db, article_id=form.id, title=form.title,
                                        description=form.description, image=image)


@router.delete('/delete', description="Delete forum")
def delete_forum(
        pk: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_session),
        service: ArticleService = Depends()
):
    return service.delete_article(pk=pk, db=db, user=user)
