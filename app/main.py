from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_database import init_db
from app.constants import mark_missed_schedules
from app.crud.medicine_crud import mark_expired_medicines
from app.mq_publisher import start_ack_subscriber, stop_ack_subscriber
from app.database.scheduler import scheduler
from app.api.v1.endpoints import router

app = FastAPI(title='MediQnect')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:8100', 'http://172.20.91.248:8100', 'ws://172.20.91.248:8100'],
  allow_credentials=True,
  allow_methods=['OPTIONS', 'POST', 'GET', 'DELETE', 'PATCH', 'PUT'],
  allow_headers=['Content-Type', 'Authorization']
)

@app.middleware('http')
async def log_requests(request: Request, call_next):
  print(f'Incoming request: {request.method} {request.url}')
  response = await call_next(request)
  print(f'Response Headers: {response.headers}')
  return response

# Initialize Database and Scheduler
@app.on_event('startup')
def on_startup():
  init_db()
  start_ack_subscriber()

def start_scheduler():
  scheduler.add_job(mark_missed_schedules, 'interval', minutes=1, id='missed_schedule_checker', replace_existing=True)
  scheduler.add_job(mark_expired_medicines, 'interval', minutes=1, id='mark_expired_medicines', replace_existing=True)
  scheduler.start()

@app.on_event('shutdown')
def shutdown_scheduler():
  scheduler.shutdown()
  stop_ack_subscriber()

# Routers
app.include_router(router)
