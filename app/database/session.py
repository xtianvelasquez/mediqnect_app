from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core import db_credentials

db_url = f'mysql+pymysql://{db_credentials['db_user']}@{db_credentials['db_host']}/{db_credentials['db_name']}'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()

  try:
    yield db
    
  finally:
    db.close()
