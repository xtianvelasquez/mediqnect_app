import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('mysql://'):
  db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)

if not db_url:
  raise ValueError('DATABASE_URL is not set.')

# Scheduler setup
jobstores = {
  'default': SQLAlchemyJobStore(url=db_url)
}
scheduler = AsyncIOScheduler(jobstores=jobstores)
