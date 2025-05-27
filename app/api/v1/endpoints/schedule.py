from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
import asyncio

from app.core import online_users
from app.database.session import get_db
from app.core import verify_token
from app.crud import get_user, check_and_send_alarms

router = APIRouter()

@router.websocket('/ws')
async def get_schedules(websocket: WebSocket, token_payload = Depends(verify_token), db: Session = Depends(get_db)):
  payload = token_payload['payload']['id']
  user = get_user(db, payload)

  if not user:
    await websocket.close(code=4004)
    return
  
  online_users.add(payload)

  try:
    while True:
      alarms = check_and_send_alarms(db, payload['id'])
      await asyncio.sleep(30)

    return alarms

  except Exception as e:
    print(f'WebSocket error: {type(e).__name__}: {e}')

  finally:
    online_users.discard(payload)
    await websocket.close()
