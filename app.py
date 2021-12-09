from fastapi import FastAPI

from apis import accounts

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },
]

app = FastAPI(
    title='Account',
    description='Psychology therapy',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(accounts.router)
