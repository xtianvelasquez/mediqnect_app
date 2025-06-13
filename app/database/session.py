import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import db_credentials

# db_url = f'mysql+pymysql://{db_credentials['db_user']}@{db_credentials['db_host']}/{db_credentials['db_name']}'
# engine = create_engine(db_url)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('mysql://'):
  db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()

  try:
    yield db
    
  finally:
    db.close()
