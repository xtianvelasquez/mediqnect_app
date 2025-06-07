from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta
import asyncio, traceback

from app.database.session import get_db
from app.core.security import verify_token, verify_ws_token
from app.services import convert_to_utc, inspect_day_duration, inspect_mins_duration, count_datetime_gap
from app.crud.auth_crud import get_user
from app.crud.alarm_crud import check_and_send_alarms
from app.crud.schedule_crud import get_specific_schedule, get_all_schedule
from app.crud.history_crud import update_specific_history
from app.schemas import Alarm_Confirm
from app.constants import SCHEDULE_STATUS, HISTORY_STATUS

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

  except WebSocketDisconnect:
    print(f'User {payload} disconnected (client closed WebSocket).')

  except Exception as e:
    print(f'Unexpected WebSocket error: {type(e).__name__}: {e}')
    traceback.print_exc()

  finally:
    if websocket.client_state.name != "DISCONNECTED":
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

  start = convert_to_utc(schedule.scheduled_datetime)
  end = data.history_datetime

  if inspect_day_duration(start.date(), end.date(), 1) and inspect_mins_duration(start.time(), end.time(), 5):
    status = HISTORY_STATUS['COMPLETED']
    updated_history = update_specific_history(db, payload, data.schedule_id, None, data.history_datetime, status)
    return updated_history
  
  else:
    status = HISTORY_STATUS['LATE']

    gap = count_datetime_gap(start.time(), end.time())

    ongoing_schedules = get_all_schedule(db, payload, data.intake_id, SCHEDULE_STATUS['ONGOING'])

    for ongoing_schedule in ongoing_schedules:
      old_dt = convert_to_utc(ongoing_schedule.scheduled_datetime)
      new_dt = old_dt + timedelta(minutes=gap)
      ongoing_schedule.scheduled_datetime = new_dt
      db.add(ongoing_schedule)

    try:
      db.commit()
    except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail=f'Failed to update schedules: {str(e)}')

    return ongoing_schedules
