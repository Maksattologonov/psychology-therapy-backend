from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    username: str


class UserCreate(BaseModel):
    name: str
    last_name: str
    anonymous_name: str
    email: str
    password: str


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
