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
from models.accounts import VerificationCode, User
from passlib.hash import bcrypt, des_crypt
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
    TokenSchema,
    UserSchema, UserCreateSchema, GetEmployeeSchema, AdminCreateSchema
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')

conn = Session()


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def get_user(cls, **filters):
        return conn.query(accounts.User).filter_by(**filters).first()

    @classmethod
    def get_users(cls, db: Session, user: UserSchema):
        schema = []
        if user.is_superuser:
            for i in db.query(accounts.User).all():
                schema.append(GetEmployeeSchema.from_orm(i))
            return schema
        else:
            raise HTTPException(detail="You don't have any permissions",
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

    @classmethod
    def get_employees(cls, db: Session, user_id: int):
        try:
            if user_id:
                return db.query(accounts.User).filter_by(id=user_id, is_employee=True).first()
            else:
                schema = []
                for i in db.query(accounts.User).filter_by(is_employee=True).all():
                    schema.append(GetEmployeeSchema.from_orm(i))
                return schema
        except Exception:
            raise HTTPException(detail="Employees not found",
                                status_code=status.HTTP_404_NOT_FOUND)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> UserSchema:
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
            user = UserSchema.parse_obj(user_data)
        except ValidationError:
            raise exception
        return user

    @classmethod
    def create_token(cls, user: accounts.User) -> TokenSchema:
        user_data = UserSchema.from_orm(user)
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
        return TokenSchema(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_user(self, user_data: UserCreateSchema):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='duplicate key value violates unique constraint',
        )
        try:
            if user_data.is_employee:
                user = accounts.User(
                    name=user_data.name,
                    last_name=user_data.last_name,
                    is_employee=user_data.is_employee,
                    is_student=False,
                    email=user_data.email,
                    hashed_password=self.hash_password(user_data.password),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    is_active=False
                )
                self.session.add(user)
                self.session.commit()
            else:
                user = accounts.User(
                    name=user_data.name,
                    last_name=user_data.last_name,
                    is_employee=user_data.is_employee,
                    email=user_data.email,
                    hashed_password=self.hash_password(user_data.password),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    is_active=False
                )
                self.session.add(user)
                self.session.commit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="The account has been successfully registered, to use please go through verification"
            )
        except sqlalchemy.exc.IntegrityError:
            raise exception

    def authenticate_user(self, email: str, password: str) -> TokenSchema:
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
                .filter(accounts.User.email == email, accounts.User.is_blocked == False)
                .first()
        )
        if not user:
            raise exception

        if not self.verify_password(password, user.hashed_password):
            raise exception
        return self.create_token(user)

    def refresh_token(self, pk: int) -> TokenSchema:
        user = self.get_user(id=pk)
        if user:
            return self.create_token(user)
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail='User not found')
        raise exception from None

    @classmethod
    def update_profile(cls, pk: int, name: str, last_name: str):
        query = conn.query(accounts.User).filter_by(id=pk)
        try:
            if name:
                query.update({"name": name})
                conn.commit()
            if last_name:
                query.update({"last_name": last_name})
                conn.commit()
            return query.first()
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Parameters cannot be empty")

    @classmethod
    def reset_password(cls, email: str, code: int, new_password: str, confirm_password: str):
        if conn.query(accounts.User).filter_by(email=email).first():
            if conn.query(VerificationCode).filter_by(code=code).first():
                if new_password == confirm_password:
                    table = accounts.User.__table__
                    stmt = table.update().values(hashed_password=cls.hash_password(new_password))
                    conn.execute(stmt)
                    conn.commit()
                    return HTTPException(status_code=status.HTTP_200_OK,
                                         detail="Password was successfully change")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Passwords do not match")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Wrong code")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Request cannot be empty")

    @classmethod
    def block_user(cls, user: UserSchema, db: Session, blocking_user: int):
        if user.is_employee and not user.is_blocked:
            b_user = db.query(User).filter_by(id=blocking_user)
            if b_user.first() and not b_user.first().is_blocked:
                b_user.update({"is_blocked": True})
                db.commit()
                return JSONResponse(status_code=status.HTTP_200_OK, content=f"Пользователь заблокирован")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="У Вас не полномочий для удаления")

    @classmethod
    def unblock_user(cls, user: UserSchema, db: Session, blocking_user: int):
        if user.is_employee and not user.is_blocked:
            b_user = db.query(User).filter_by(id=blocking_user)
            if b_user.first() and b_user.first().is_blocked:
                b_user.update({"is_blocked": False})
                db.commit()
                return JSONResponse(status_code=status.HTTP_200_OK, content=f"Пользователь разблокирован")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="У Вас не полномочий для разблокировки")

    def register_superuser(self, user_data: AdminCreateSchema):
        try:
            if user_data.secret_key == config("JWT_SECRET"):
                user = accounts.User(
                    name=user_data.name,
                    last_name=user_data.last_name,
                    is_employee=False,
                    is_superuser=True,
                    is_student=False,
                    email=user_data.email,
                    hashed_password=self.hash_password(user_data.password),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                    is_active=False
                )
                self.session.add(user)
                self.session.commit()
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content="The account has been successfully registered, to use please go through verification"
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='duplicate key value violates unique constraint',
            )


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
                cls.delete(user=email)
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
    def update_code(cls, email: str, code: int):
        conn.query(cls.model).filter_by(user=email).update({"code": code})
        conn.commit()

    @classmethod
    def create_record(cls, user: str, code: int):
        email = AuthService.get_user(email=user)
        query = cls.model(user=user, code=code)
        conn.add(query)
        conn.commit()

    @classmethod
    async def send_email_async(cls, email: str):
        record = conn.query(accounts.User).filter_by(email=email).first()
        if record:
            bar = Template(raw)
            code = cls.verification_code(email=email)
            template = bar.render(messages={'name': f"{record.name + ' ' + record.last_name}", 'code': code})
            message = EmailMessage()
            message['Subject'] = f'Здравствуйте {record.name + " " + record.last_name}!'
            message['From'] = config("MAIL_FROM")
            message['To'] = email
            message.add_alternative(template, subtype='html')
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login(config("MAIL_FROM"), config("MAIL_PASSWORD"))
            smtp.send_message(message)
            smtp.quit()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content="Message sent successfully"
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    @staticmethod
    def generate_code() -> int:
        return random.randint(100000, 999999)

    @classmethod
    def verification_code(cls, email: str):
        code = cls.generate_code()
        if not cls.check_code(code=code):
            if cls.check_code(user=email):
                cls.update_code(email=email, code=code)
            else:
                cls.create_record(user=email, code=code)
        return code
