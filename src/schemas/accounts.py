import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, validator
from starlette import status


def must_be_manas_account(v: str) -> str:
    if len(v) == 23:
        if re.findall('@manas.edu.kg', v):
            return v
    raise ValueError("Incorrectly entered email")


class BaseUserSchema(BaseModel):
    email: str
    password: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)


class UserCreateSchema(BaseModel):
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


class UserSchema(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class EmailSchema(BaseModel):
    email: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)

    class Config:
        orm_mode = True


class VerifiedCodeSchema(BaseModel):
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


class RefreshTokenSchema(BaseModel):
    token: str


class UserGetSchema(BaseModel):
    id: Optional[int]
    email: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    anonymous_name: Optional[str]

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    anonymous_name: Optional[str]

    class Config:
        orm_mode = True


class ResetPasswordSchema(BaseModel):
    email: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)
    code: int
    new_password: str
    confirm_password: str

    @validator('new_password', 'confirm_password')
    def validate_password(cls, v):
        if len(v) > 8:
            return v
        raise ValueError("Password must be more than 8 characters")
