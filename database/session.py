from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core import db_user, db_password, db_host, db_name

db_url = f'mysql+pymysql://{db_user}@{db_host}/{db_name}'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()

  try:
    yield db
    
  finally:
    db.close()
