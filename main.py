from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()

router.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:8100'],  # Ionic default
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)
