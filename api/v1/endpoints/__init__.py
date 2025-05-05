from fastapi import APIRouter
from . import auth, user, prescription

router = APIRouter()

router.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
router.include_router(user.router, tags=['user'])
router.include_router(prescription.router, tags=['prescription'])
