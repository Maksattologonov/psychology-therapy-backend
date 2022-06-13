import os

from fastapi import APIRouter
from starlette.responses import FileResponse
from decouple import config

router = APIRouter(
    prefix='',
    include_in_schema=True,
    tags=['media']
)
path = str(config('BASE_URL'))


@router.get('/', response_class=FileResponse, responses={200: {"description": "Get media files", "content": {
    "image/jpeg": {"example": "To query params write `Hostname/?media={path your wanted file}` "}}}})
def get_forum_images(media: str):
    image_url = os.path.join(path.strip(), media.strip())
    if os.path.exists(image_url):
        return FileResponse(image_url, media_type="image/jpeg")
