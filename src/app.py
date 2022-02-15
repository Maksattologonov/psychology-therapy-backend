from fastapi import FastAPI
from apis.accounts import router
from apis.forum import router as forum_router
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='common/templates')


def get_application() -> FastAPI:
    application = FastAPI(
        title='Account',
        description='Psychology therapy',
        version='1.0.0',
    )
    application.include_router(router=router)
    application.include_router(router=forum_router)
    return application


app = get_application()
