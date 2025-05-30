from fastapi import APIRouter,  HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core import verify_token
from app.crud import get_user, get_all_history
from app.schemas import Intake_History_Read

router = APIRouter()

@router.get('/histories', response_model=List[Intake_History_Read], status_code=200)
def get_histories(token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')
  
  history = get_all_history(db, payload)

  return history
