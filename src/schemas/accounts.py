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
    is_employee: Optional[bool] = False
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


class AdminCreateSchema(BaseModel):
    name: str
    last_name: str
    secret_key: str
    email: str
    _normalize_name = validator('email', allow_reuse=True)(must_be_manas_account)
    password: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    email: str
    is_blocked: bool
    is_employee: bool
    is_superuser: bool

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
    is_employee: Optional[str]
    is_student: Optional[str]
    is_superuser: Optional[str]

    class Config:
        orm_mode = True


class GetEmployeeSchema(BaseModel):
    id: int
    email: str
    name: str
    last_name: str

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[str]
    last_name: Optional[str]

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
