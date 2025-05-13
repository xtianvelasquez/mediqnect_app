from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.enums import Dose_Component_Enum

router = APIRouter()

@router.get('/components', response_model=List[dict])
def medicine_form():
  return [{'value': component.value} for component in Dose_Component_Enum]
