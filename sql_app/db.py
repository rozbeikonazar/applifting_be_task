"Database setup"
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./data/data.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:100173Rr@localhost/applifting_be_task"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    "Create independent database session for each request"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
