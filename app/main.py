from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_database import init_db
from app.crud.alarm_crud import mark_missed_schedules
from app.database.scheduler import scheduler
from app.api.v1.endpoints import router

app = FastAPI(title='MediQnect')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:8100', 'http://192.168.147.30:8100', 'ws://192.168.147.30:8100'],
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

def start_scheduler():
  scheduler.add_job(mark_missed_schedules, 'interval', minutes=1, id='missed_schedule_checker', replace_existing=True)
  scheduler.start()

@app.on_event('shutdown')
def shutdown_scheduler():
  scheduler.shutdown()

# Routers
app.include_router(router)
