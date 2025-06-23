from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from zoneinfo import ZoneInfo

from app.models import Token
from app.core.security import decode_token

def store_token(db: Session, token: str):
  try:
    decoded_token = decode_token(token)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Token decoding failed: {str(e)}')
  
  try:
    issued_at = datetime.fromtimestamp(decoded_token['iat'], tz=ZoneInfo('Asia/Manila'))
    expires_at = datetime.fromtimestamp(decoded_token['exp'], tz=ZoneInfo('Asia/Manila'))

    new_token = Token(
      token_hash=token,
      issued_at=issued_at,
      expires_at=expires_at,
      user_id=decoded_token['id']
    )

    db.add(new_token)
    db.commit()
    db.refresh(new_token)

    if not new_token:
      raise HTTPException(status_code=500, detail='Token could not be stored.')
    
    return new_token.token_hash
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
  
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')

def logout_token(db: Session, token: str):
  try:
    stored_token = db.query(Token).filter(Token.token_hash == token).first()
    
    if not stored_token:
      raise HTTPException(status_code=404, detail='Token not found.')
    
    stored_token.is_active=False
    stored_token.revoked_at=datetime.now(ZoneInfo('Asia/Manila')).replace(second=0, microsecond=0)
    db.commit()
    db.refresh(stored_token)

    return {'message': 'You have been logged out.'}
  
  except SQLAlchemyError as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
  
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
