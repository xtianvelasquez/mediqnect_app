from fastapi import APIRouter
from app.api.v1.endpoints import auth

router = APIRouter()

router.include_router(auth.router, tags=['Auth'])
