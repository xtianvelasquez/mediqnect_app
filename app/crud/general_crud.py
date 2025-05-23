from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Compartment, Medicine_Form, Dose_Component, Statuses

def get_specific_status(db: Session, status):
  try:
    return db.query(Statuses).filter(Statuses.status_name == status).first()

  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_medicine_form(db: Session):
  try:
    return db.query(Medicine_Form).all()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
  
def get_dose_component(db: Session):
  try:
    return db.query(Dose_Component).all()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_tablet_compartments(db: Session):
  try:
    return db.query(Compartment).filter(Compartment.set_id == 1).all()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_syrups_compartments(db: Session):
  try:
    return db.query(Compartment).filter(Compartment.set_id == 2).all()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
