from datetime import datetime, timedelta
import random
import smtplib
import sqlalchemy

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from email.message import EmailMessage
from decouple import config
from jinja2 import Template
from starlette.responses import JSONResponse
from common.message import raw
from models.accounts import VerificationCode
from passlib.hash import bcrypt
from fastapi import status
from pydantic import ValidationError
from core.database import get_session, Session
from core.settings import settings
from models import accounts
from jose import (
    jwt,
    JWTError
)
from schemas.accounts import (
    Token,
    User, UserCreate
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')

conn = Session()


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not  validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception
        user_data = payload.get('user')
        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception
        return user

    @classmethod
    def create_token(cls, user: accounts.User) -> Token:
        user_data = User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expirations),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_user(self, user_data: UserCreate):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='duplicate key value violates unique constraint',
        )
        try:
            user = accounts.User(
                name=user_data.name,
                last_name=user_data.last_name,
                anonymous_name=user_data.anonymous_name,
                email=user_data.email,
                hashed_password=self.hash_password(user_data.password),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=False
            )
            self.session.add(user)
            self.session.commit()
            SendMessageWhenCreateUser.send_email_async(email_to=user_data.email, name=user_data.name,
                                                       last_name=user_data.last_name)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="The account has been successfully registered, to use please go through verification"
            )
        except sqlalchemy.exc.IntegrityError:
            raise exception

    def authenticate_user(self, email: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        user = (
            self.session
                .query(accounts.User)
                .filter(accounts.User.email == email)
                .first()
        )
        if not user:
            raise exception

        if not self.verify_password(password, user.hashed_password):
            raise exception
        return self.create_token(user)

    def refresh_token(self, token: str) -> Token:
        user = self.validate_token(token)
        if user:
            return self.create_token(user)
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail='User not found')
        raise exception from None


class SendMessageWhenCreateUser:
    model = VerificationCode

    @classmethod
    def activate_user(cls, email: str, code: int):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Activation code entered incorrectly',
        )
        if conn.query(cls.model).filter_by(user=email, code=code).first():
            user = conn.query(accounts.User).filter_by(email=email).first()
            if not user.is_active:
                user.is_active = True
                conn.commit()
                return AuthService.create_token(user)
        raise exception

    @classmethod
    def check_code(cls, **filters):
        return conn.query(cls.model).filter_by(**filters).all()

    @classmethod
    def delete(cls, **filters):
        conn.query(cls.model).filter_by(**filters).delete()
        conn.commit()

    @classmethod
    def update_code(cls, **filters):
        table = cls.model.__table__
        stmt = table.update().values(**filters)
        conn.execute(stmt)
        conn.commit()

    @classmethod
    def create_record(cls, **filters):
        record = cls.model(**filters)
        conn.add(record)
        conn.commit()

    @classmethod
    async def send_email_async(cls, email_to: str, name: str, last_name: str):
        bar = Template(raw)
        code = cls.verification_code(email=email_to)
        template = bar.render(messages={'name': f"{name + ' ' + last_name}", 'code': code})
        message = EmailMessage()
        message['Subject'] = f'Здравствуйте {name + " " + last_name}!'
        message['From'] = config("MAIL_FROM")
        message['To'] = email_to
        message.add_alternative(template, subtype='html')
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(config("MAIL_FROM"), config("MAIL_PASSWORD"))
        await smtp.send_message(message)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Message sent successfully"
        )

    @staticmethod
    def generate_code() -> int:
        return random.randint(100000, 999999)

    @classmethod
    def verification_code(cls, email: str):
        code = cls.generate_code()
        if not cls.check_code(code=code):
            if cls.check_code(user=email):
                cls.update_code(code=code)
            cls.create_record(user=email, code=code)
        return code
