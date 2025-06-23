from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio, traceback

from app.database.session import get_db, SessionLocal
from app.core.security import verify_token, verify_ws_token
from app.services import convert_to_tz
from app.crud.auth_crud import get_user
from app.crud.alarm_crud import check_and_send_alarms
from app.crud.prescription_crud import get_specific_intake
from app.crud.schedule_crud import get_specific_schedule
from app.crud.history_crud import update_specific_history
from app.schemas import Alarm_Confirm
from app.constants import SCHEDULE_STATUS, HISTORY_STATUS

router = APIRouter()

@router.websocket('/ws')
async def get_schedules(websocket: WebSocket):
  await websocket.accept()

  token = websocket.query_params.get('token')

  if not token:
    await websocket.close(code=1008)
    return

  try:
    # Use a temporary session just for token verification
    with SessionLocal() as db:
      token_payload = verify_ws_token(db, token)
      payload = token_payload.get('payload', {}).get('id')
      user = get_user(db, payload)

    if not user:
      await websocket.close(code=4004)
      return
    
    print(f'User {payload} connected via WebSocket!')
    
    while True:
      with SessionLocal() as db:
        alarms = check_and_send_alarms(db, payload)
        print(f'Sending alarms: {alarms}')
        await websocket.send_json({'alarms': jsonable_encoder(alarms)})

      now = datetime.now(ZoneInfo('Asia/Manila'))
      seconds_to_next_minute = 60 - now.second - now.microsecond / 1_000_000
      await asyncio.sleep(seconds_to_next_minute)

  except WebSocketDisconnect:
    print(f'User {payload} disconnected (client closed WebSocket).')

  except Exception as e:
    print(f'Unexpected WebSocket error: {type(e).__name__}: {e}')
    traceback.print_exc()

  finally:
    if websocket.client_state.name != 'DISCONNECTED':
      await websocket.close()
    print(f'User {payload} fully disconnected.')

@router.post('/confirm', status_code=200)
def confirm_alarm(
  data: Alarm_Confirm,
  token_payload=Depends(verify_token),
  db: Session=Depends(get_db)):

  payload = token_payload.get('payload', {}).get('id')
  user = get_user(db, payload)

  if not user:
    raise HTTPException(status_code=404, detail='User not found.')

  schedule = get_specific_schedule(db, payload, None, data.schedule_id)
  if not schedule:
    raise HTTPException(status_code=404, detail='Schedule not found.')

  intake = get_specific_intake(db, payload, schedule.intake_id)
  if not intake:
    raise HTTPException(status_code=404, detail='Intake not found.')
  
  if not data.history_datetime:
    raise HTTPException(status_code=400, detail='history_datetime is required.')

  if intake.medicine.net_content <= 0:
    raise HTTPException(status_code=400, detail='Medicine is already empty. Cannot confirm intake.')

  if intake.medicine.net_content < intake.dose:
    raise HTTPException(status_code=400, detail='Not enough medicine left to confirm this dose.')

  confirmation_datetime = convert_to_tz(data.history_datetime)
  status = HISTORY_STATUS['COMPLETED']

  updated_history = update_specific_history(db, payload, data.schedule_id, None, confirmation_datetime, status)
  schedule.status_id = SCHEDULE_STATUS['ENDED']
  intake.medicine.net_content -= intake.dose

  try:
    db.commit()
    db.refresh(schedule)
    db.refresh(intake)
  except Exception as e:
    db.rollback()
    print(traceback.format_exc())
    raise HTTPException(status_code=500, detail=f'Failed to update alarm confirmation: {str(e)}')
  
  return updated_history
