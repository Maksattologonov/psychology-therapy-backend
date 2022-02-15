from decouple import config
from fastapi import Depends, APIRouter
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordRequestForm, APIKeyHeader
from fastapi_mail import ConnectionConfig

from services.accounts import SendMessageWhenCreateUser, oauth2_scheme
from schemas.accounts import (
    User,
    UserCreate,
    Token, Email, VerifiedCode, BaseUser, RefreshToken
)
from services.accounts import AuthService, get_current_user

router = APIRouter(
    prefix='/auth',
)


@router.post('/sign-up', response_model=Token)
def sign_up(
        user_data: UserCreate,
        service: AuthService = Depends()
):
    return service.register_user(user_data)


@router.post('/sign-in', response_model=Token)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(form_data.username, form_data.password)


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


@router.post('/send-email/')
def send_email_asynchronous(response_model: Email, service: SendMessageWhenCreateUser = Depends()):
    return service.send_email_async(email_to=response_model.email, name=response_model.name,
                                    last_name=response_model.last_name)


@router.post('/verified-account', response_model=Token)
def verified_account(form_data: VerifiedCode, service: SendMessageWhenCreateUser = Depends()):
    return service.activate_user(email=form_data.email, code=form_data.code)


@router.post('/refresh-token', response_model=Token)
def refresh_token(form_data: RefreshToken, service: AuthService = Depends()):
    return service.refresh_token(token=form_data.token)
