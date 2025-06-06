from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_database import init_db
from app.api.v1.endpoints import router

app = FastAPI(title='MediQnect')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],  # Ionic default
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# Initialize Database
@app.on_event('startup')
def on_startup():
  init_db()

# Routers
app.include_router(router)
