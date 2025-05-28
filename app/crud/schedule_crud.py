from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import mqtt_credentials
from app.database.session import SessionLocal
from app.core import online_users
from app.constants import SCHEDULE_STATUS
from app.services import convert_datetime
from app.models import Medicine_Compartment, Schedule, Color

mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(mqtt_credentials['mqtt_broker'], mqtt_credentials['mqtt_port'])

def check_and_send_alarms(db: Session, user_id: int):
  now = datetime.now(ZoneInfo('UTC')).replace(second=0, microsecond=0)
  print(f'Checking alarms for user {user_id} at {convert_datetime(now)}') # Testing

  sent_alarms = []

  schedules = db.query(Schedule).filter(Schedule.user_id == user_id, Schedule.scheduled_datetime == now).all()
  for schedule in schedules:
    medicine_compartment = db.query(Medicine_Compartment).filter(Medicine_Compartment.medicine_id == schedule.intake.medicine_id).first()

    if medicine_compartment:
      mqtt_payload = {
        'user_id': schedule.user_id,
        'intake_id': schedule.intake_id,
        'schedule_id': schedule.schedule_id,
        'scheduled_datetime': schedule.scheduled_datetime,
        'medicine_name': medicine_compartment.medicine.medicine_name,
        'compartment_id': medicine_compartment.compartment.compartment_id
      }

      sent_alarms.append(mqtt_payload)
      topic = f'alarm/{schedule.user_id}'

      try:
        print(f'[ALARM SENT] Published to {topic} → {mqtt_payload}')
        mqtt_client.publish(topic, json.dumps(mqtt_payload))
      except Exception as e:
        print(f'MQTT error: {e}, reconnecting...')
        mqtt_client.reconnect()
        mqtt_client.publish(topic, json.dumps(mqtt_payload))

  return sent_alarms

def get_all_schedule(db: Session, user_id: int):
  sent_schedules = []

  schedules = db.query(Schedule).filter(Schedule.user_id == user_id, Schedule.status_id == SCHEDULE_STATUS['ONGOING']).all()
  for schedule in schedules:
    medicine_compartment = db.query(Medicine_Compartment).filter(Medicine_Compartment.medicine_id == schedule.intake.medicine_id).first()
    color = db.query(Color).filter(Color.color_id == schedule.intake.color_id).first()

    if medicine_compartment:
      schedule_payload = {
        'user_id': schedule.user_id,
        'intake_id': schedule.intake_id,
        'scheduled_datetime': schedule.scheduled_datetime,
        'schedule_id': schedule.schedule_id,
        'medicine_name': medicine_compartment.medicine.medicine_name,
        'color_name': color.color_name
      }

      sent_schedules.append(schedule_payload)

  return sent_schedules

def scheduled_alarm_task():
  db: Session = SessionLocal()
  users = db.query(Schedule.user_id).distinct().all()

  for user in users:
    if user.user_id in online_users:
      check_and_send_alarms(db, user.user_id)

  db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_alarm_task, 'interval', minutes=1)

def start_scheduler():
  scheduler.start() if len(online_users) >= 1 else None

start_scheduler