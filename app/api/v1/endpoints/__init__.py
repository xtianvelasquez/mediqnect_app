from fastapi import APIRouter
from app.api.v1.endpoints import auth, user, prescription

router = APIRouter()

router.include_router(auth.router, tags=['Auth'])
router.include_router(user.router, tags=['User'])
