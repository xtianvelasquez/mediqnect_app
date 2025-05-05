from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user, auth

app = FastAPI(title='MediQnect')

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:8100'],  # Ionic default
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

# Include routers
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(user.router, prefix='/user', tags=['user'])
