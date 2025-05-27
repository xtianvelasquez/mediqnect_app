from fastapi import APIRouter
from app.api.v1.endpoints import auth, general, prescription, schedule

router = APIRouter()

router.include_router(auth.router, tags=['Auth'])
router.include_router(general.router, tags=['General'])
router.include_router(prescription.router, tags=['Prescription'])
router.include_router(schedule.router, tags=['Schedule'])
