from pydantic import BaseSettings
from decouple import config


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = config('DB_URL')

    jwt_secret: str = config('JWT_SECRET')
    jwt_algorithm: str = 'HS256'
    jwt_expirations: int = 86400


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
