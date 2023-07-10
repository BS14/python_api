from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#SQLACLEHMY_DATABASE_URL = 'postgresql://<USERNAME>:<PASSWORD>@<IP-ADDDRESS>/<DATABASE-NAME>'
SQLACLEHMY_DATABASE_URL = 'postgresql://python_api:password@127.0.0.1/python_api'

engine = create_engine(SQLACLEHMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()