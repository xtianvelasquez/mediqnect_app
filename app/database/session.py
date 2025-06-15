import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('mysql://'):
  db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)

if not db_url:
  raise ValueError('DATABASE_URL is not set.')

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()

  try:
    yield db
    
  finally:
    db.close()
