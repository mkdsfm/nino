from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URI or settings.SQLITE_DATABASE_URI,
    connect_args={"check_same_thread": False} if settings.DB_TYPE == "sqlite" else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency function to get DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
