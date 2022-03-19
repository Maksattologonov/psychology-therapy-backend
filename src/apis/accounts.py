from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, APIKeyHeader

from services.accounts import SendMessageWhenCreateUser, oauth2_scheme
from schemas.accounts import (
    UserSchema, UserCreateSchema,
    TokenSchema, EmailSchema, VerifiedCodeSchema, BaseUserSchema, RefreshTokenSchema, UserUpdateSchema,
    UserGetSchema, ResetPasswordSchema
)
from services.accounts import AuthService, get_current_user

router = APIRouter(
    prefix='/auth',
    include_in_schema=True,
    tags=['accounts']
)


@router.post('/sign-up', response_model=TokenSchema)
def sign_up(
        user_data: UserCreateSchema,
        service: AuthService = Depends()
):
    return service.register_user(user_data)


@router.post('/sign-in', response_model=TokenSchema)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(form_data.username, form_data.password)


@router.get('/user', response_model=UserGetSchema)
def get_user(user: UserSchema = Depends(get_current_user)):
    return AuthService.get_user(id=user.id)


@router.post('/send-email')
async def send_email_asynchronous(response_model: EmailSchema):
    return await SendMessageWhenCreateUser.send_email_async(email=response_model.email)


@router.post('/verified-account', response_model=TokenSchema)
def verified_account(form_data: VerifiedCodeSchema, service: SendMessageWhenCreateUser = Depends()):
    return service.activate_user(email=form_data.email, code=form_data.code)


@router.get('/refresh-token')
def refresh_token(user: UserSchema = Depends(get_current_user), service: AuthService = Depends()):
    return service.refresh_token(pk=user.id)


@router.patch('/update-profile', response_description="Profile updated")
def update_profile(form: UserUpdateSchema = Depends(), user: UserSchema = Depends(get_current_user)):
    return AuthService.update_profile(pk=user.id, name=form.name, last_name=form.last_name,
                                      anonymous_name=form.anonymous_name)


@router.put("/reset-password", response_description="Password successfully changed")
def reset_password(form: ResetPasswordSchema, user: UserSchema = Depends(get_current_user)):
    return AuthService.reset_password(user_id=user.id, code=form.code, new_password=form.new_password,
                                      confirm_password=form.confirm_password)
