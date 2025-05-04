from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_user = 'root'
db_password = None
db_host = 'localhost'
db_name = 'mediqnect'
db_url = f'mysql+pymysql://{db_user}@{db_host}/{db_name}'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()

  try:
    yield db
    
  finally:
    db.close()