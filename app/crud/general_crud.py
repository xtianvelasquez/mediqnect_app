from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Color, Compartment, Medicine_Form, Dose_Component, Medicine

def get_specific_color(db: Session, color_name: str):
  try:
    return db.query(Color).filter(Color.color_name == color_name).first()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_medicine_forms(db: Session):
  try:
    return db.query(Medicine_Form).all()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
  
def get_dose_components(db: Session):
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

def get_specific_compartment(db: Session, compartment_id: int):
  try:
    return db.query(Compartment).filter(Compartment.compartment_id == compartment_id).first()

  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def get_specific_medicine(db: Session, user_id: int, medicine_id: int):
  try:
    return db.query(Medicine).filter(Medicine.user_id == user_id, Medicine.medicine_id == medicine_id).first()
  
  except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
