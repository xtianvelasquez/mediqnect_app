from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:8100"],  # Ionic default
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
