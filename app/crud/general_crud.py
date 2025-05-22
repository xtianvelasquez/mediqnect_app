from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Compartment

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
