from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from core.database import (
    url as SQLALCHEMY_DATABASE_URL, get_session, Base,
)

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine("sqlite:///./test.db", pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db(cls):
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
