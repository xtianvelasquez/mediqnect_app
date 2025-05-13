from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.enums import Medicine_Form_Enum

router = APIRouter()

@router.get('/forms', response_model=List[dict])
def medicine_form():
  return [{'value': form.value} for form in Medicine_Form_Enum]
