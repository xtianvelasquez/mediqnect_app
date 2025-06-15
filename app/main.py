from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_database import init_db
from app.api.v1.endpoints import router

app = FastAPI(title='MediQnect')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:8100', 'http://192.168.58.30:8100', 'ws://192.168.58.30:8100'],
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

# Initialize Database
@app.on_event('startup')
def on_startup():
  init_db()

# Routers
app.include_router(router)
