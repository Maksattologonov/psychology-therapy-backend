from decouple import config
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import ConnectionConfig

from services.accounts import SendMessageWhenCreateUser
from schemas.accounts import (
    User,
    UserCreate,
    Token, Email, VerifiedCode, BaseUser
)
from services.accounts import AuthService, get_current_user

conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME"),
    MAIL_PASSWORD=config('MAIL_PASSWORD'),
    MAIL_FROM=config('MAIL_FROM'),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME=config('MAIL_FROM_NAME'),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
)

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
        form_data: BaseUser,
        service: AuthService = Depends()
):
    return service.authenticate_user(form_data.email, form_data.password)


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
def refresh_token(form_data: BaseUser, service: AuthService = Depends()):
    return service.refresh_token(email=form_data.email, password=form_data.password)