from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from endpoints import DATABASE_URL
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    '''Dependency function to get a database session
    This ensures each request gets a new session, and the session is closed
    properly afterwards.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # clean up after each request
