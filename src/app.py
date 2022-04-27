from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apis.accounts import router
from apis.forum import router as forum_router
from apis.article import router as article_router
from apis.appointments import router as appointments_router
from images.media import router as media_router
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='common/templates')

origins = [
    "http://localhost:3000",
    "https://localhost:8000",
    "http://localhost:8000",
    "http://localhost:8080",
]


def get_application() -> FastAPI:
    application = FastAPI(
        title='Account',
        description='Psychology therapy',
        version='1.0.0',
    )
    application.include_router(router=router)
    application.include_router(router=forum_router)
    application.include_router(router=article_router)
    application.include_router(router=appointments_router)
    application.include_router(router=media_router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()
