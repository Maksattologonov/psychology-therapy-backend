import re

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


def must_be_manas_account(v: str) -> str:
    if len(v) == 23:
        if re.findall('@manas.edu.kg', v):
            return v
    raise ValueError("Incorrectly entered email")


class BaseUser(BaseModel):
    email: str
    password: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)


class UserCreate(BaseModel):
    name: str
    last_name: str
    anonymous_name: str
    email: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)
    password: str

    class Config:
        orm_mode = True

    @validator('password')
    def validate_password(cls, v):
        if len(v) > 8:
            return v
        raise ValueError("Password must be more than 8 characters")


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class Email(BaseModel):
    id: int
    email: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)
    name: str
    last_name: str


class VerifiedCode(BaseModel):
    email: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)
    code: int

    @validator("code")
    def validate_code(cls, v):
        exception = HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail='The activation code must be 6 digits',
        )
        if len(str(v)) == 6:
            return v
        raise exception
