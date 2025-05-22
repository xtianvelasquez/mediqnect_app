from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import get_tablet_compartments, get_syrups_compartments
from app.enums import Medicine_Form_Enum, Dose_Component_Enum
from app.schemas import Common_Response, Compartment_Read

router = APIRouter()

@router.get('/forms', response_model=List[Common_Response], status_code=200)
def medicine_form():
  return [Common_Response(value=form.value) for form in Medicine_Form_Enum]

@router.get('/components', response_model=List[Common_Response], status_code=200)
def dose_component():
  return [Common_Response(value=component.value) for component in Dose_Component_Enum]

@router.get('/compartments', response_model=List[Compartment_Read], status_code=200)
def compartments(db: Session = Depends(get_db)):
  tablet_data = [
    {'compartment_name': compartment.compartment_name, 'status_name': compartment.status.status_name, 'set_name': compartment.set.set_name, 'compartment_id': compartment.compartment_id}
    for compartment in get_tablet_compartments(db)
  ]

  syrups_data = [
    {'compartment_name': compartment.compartment_name, 'status_name': compartment.status.status_name, 'set_name': compartment.set.set_name, 'compartment_id': compartment.compartment_id}
    for compartment in get_syrups_compartments(db)
  ]
  
  return tablet_data + syrups_data
