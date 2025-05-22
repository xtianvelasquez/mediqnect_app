from fastapi import APIRouter
from app.api.v1.endpoints import auth, general

router = APIRouter()

router.include_router(auth.router, tags=['Auth'])
router.include_router(general.router, tags=['General'])
