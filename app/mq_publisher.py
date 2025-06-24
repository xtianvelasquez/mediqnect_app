from app.database.session import SessionLocal
from datetime import datetime
from zoneinfo import ZoneInfo
import paho.mqtt.client as mqtt
import json, ssl, time

from app.crud.auth_crud import get_user
from app.crud.prescription_crud import get_specific_intake
from app.crud.schedule_crud import get_specific_schedule
from app.crud.history_crud import confirm_history
from app.constants import SCHEDULE_STATUS, HISTORY_STATUS

# HiveMQ Cloud details
BROKER = '226d38fc646f4e549353211b488ed337.s1.eu.hivemq.cloud'
PORT = 8883
USERNAME = 'esp32'
PASSWORD = 'Mediqnect-2025'

def publish_message(message: str, topic: str):
  client = mqtt.Client()
  client.username_pw_set(USERNAME, PASSWORD)
  client.tls_set(tls_version=ssl.PROTOCOL_TLS)

  try:
    client.connect(BROKER, PORT)
    client.loop_start()
    result = client.publish(topic, message, qos=1)
    result.wait_for_publish()
    time.sleep(1)
    client.loop_stop()
    client.disconnect()
    print(f"Published message: '{message}' to topic: '{topic}'")
  except Exception as e:
    print(f'MQTT publish failed: {e}')

def on_message(client, userdata, message):
  try:
    payload = json.loads(message.payload.decode())

    print(f'[MQTT] ACK received on topic {message.topic}: {payload}')
    user_id = payload.get('user_id')
    schedule_id = payload.get('schedule_id')
    status = payload.get('status')

    if not (user_id and schedule_id):
      print('[MQTT] Incomplete payload data.')
      return
    
    with SessionLocal() as db:
      user = get_user(db, user_id)

      if status != 'missed':
        if not user:
          print(f"[MQTT] User not found with ID: {user_id}")
          return
        
        schedule = get_specific_schedule(db, user.user_id, None, schedule_id)
        if not schedule:
          print(f'[MQTT] Schedule not found with ID: {schedule_id}')
          return
        
        intake = get_specific_intake(db, user.user_id, schedule.intake_id)
        if not intake:
          print(f'[MQTT] Intake not found for schedule ID: {schedule_id}')
          return
        
        if intake.medicine.net_content < intake.dose:
          print('[MQTT] Not enough medicine left to confirm dose.')
          return

        confirmation_datetime = datetime.now(ZoneInfo('Asia/Manila')).replace(second=0, microsecond=0)
        confirm_history(
          db,
          user_id=user.user_id,
          schedule_id=schedule.schedule_id,
          confirmation_datetime=confirmation_datetime,
          status_id=HISTORY_STATUS['COMPLETED'])
        
        schedule.status_id = SCHEDULE_STATUS['ENDED']
        intake.medicine.net_content -= intake.dose

        try:
          db.commit()
          db.refresh(schedule)
          db.refresh(intake)
          print('[MQTT] ACK processed successfully.')
        except Exception as e:
          db.rollback()
          print(f'[MQTT] Database commit failed: {e}')
          
      else:
        print('[MQTT] ACK (missed) processed successfully.')

        print('[MQTT] ACK processed successfully.')
  except Exception as e:
    print(f'[MQTT] Error processing message: {e}')

def start_ack_subscriber():
  client = mqtt.Client()
  client.username_pw_set(USERNAME, PASSWORD)
  client.tls_set()
  client.on_message = on_message

  client.connect(BROKER, PORT)
  client.subscribe('mediqnect/ack/DISP-A400F667B4FC')
  print('[MQTT] Subscribed to mediqnect/ack/DISP-A400F667B4FC')

  client.loop_start()

mqtt_client = None

def start_ack_subscriber():
  global mqtt_client

  mqtt_client = mqtt.Client()
  mqtt_client.username_pw_set(USERNAME, PASSWORD)
  mqtt_client.tls_set()
  mqtt_client.on_message = on_message

  mqtt_client.connect(BROKER, PORT)
  mqtt_client.subscribe('mediqnect/ack/DISP-A400F667B4FC')
  print('[MQTT] Subscribed to mediqnect/ack/DISP-A400F667B4FC')
  mqtt_client.loop_start()

def stop_ack_subscriber():
  global mqtt_client
  
  if mqtt_client:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print('[MQTT] Disconnected cleanly.')
