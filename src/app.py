from fastapi import FastAPI
from apis import accounts
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='common/templates')
app = FastAPI(
    title='Account',
    description='Psychology therapy',
    version='1.0.0',
)
app.include_router(accounts.router)
