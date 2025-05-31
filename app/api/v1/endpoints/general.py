from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.crud import get_medicine_forms, get_dose_components, get_tablet_compartments, get_syrups_compartments
from app.schemas import Form_Base, Component_Base, Compartment_Read

router = APIRouter()

@router.get('/get/forms', response_model=List[Form_Base], status_code=200)
def medicine_form(db: Session = Depends(get_db)):
  return [
    {'form_id': form.form_id, 'form_name': form.form_name}
    for form in get_medicine_forms(db)
  ]

@router.get('/get/components', response_model=List[Component_Base], status_code=200)
def dose_component(db: Session = Depends(get_db)):
  return [
    {'component_id': component.component_id, 'component_name': component.component_name}
    for component in get_dose_components(db)
  ]

@router.get('/get/compartments', response_model=List[Compartment_Read], status_code=200)
def compartments(db: Session = Depends(get_db)):
  tablet_data = [
    {'compartment_name': compartment.compartment_name,
     'compartment_id': compartment.compartment_id,
     'status_name': compartment.status.status_name,
     'set_name': compartment.set.set_name,}

    for compartment in get_tablet_compartments(db)
  ]

  syrups_data = [
    {'compartment_name': compartment.compartment_name,
     'compartment_id': compartment.compartment_id,
     'status_name': compartment.status.status_name,
     'set_name': compartment.set.set_name,}
     
    for compartment in get_syrups_compartments(db)
  ]
  
  return tablet_data + syrups_data
