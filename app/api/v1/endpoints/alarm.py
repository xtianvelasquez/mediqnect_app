from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
import asyncio, traceback

from app.database.session import get_db
from app.core.security import verify_ws_token
from app.crud import get_user, check_and_send_alarms

router = APIRouter()

@router.websocket('/ws')
async def get_schedules(websocket: WebSocket, db: Session = Depends(get_db)):
  await websocket.accept()

  token = websocket.query_params.get('token')
  if not token:
    await websocket.close(code=1008)
    return
  
  try:
    token_payload = verify_ws_token(db, token)
    payload = token_payload.get('payload', {}).get('id')

  except Exception as e:
    print(f'Token error: {e}')
    await websocket.close(code=1008)
    return

  print(f'User {payload} connected via WebSocket!')
  user = get_user(db, payload)

  if not user:
    await websocket.close(code=4004)
    return

  try:
    while True:
      alarms = check_and_send_alarms(db, payload)
      print(f'Sending alarms: {alarms}')
      await websocket.send_json({'alarms': alarms})
      await asyncio.sleep(60)

  except Exception as e:
    print(f'WebSocket error: {type(e).__name__}: {e}')
    traceback.print_exc()

  finally:
    print(f'User {payload} disconnected!')
    await websocket.close()
