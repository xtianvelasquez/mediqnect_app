import paho.mqtt.client as mqtt

broker = "localhost"  # Change to your broker IP if needed
port = 1883  # Default MQTT port

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, port)

topic = "test/topic"
message = "Hello MQTT!"
client.publish(topic, message)
print(f"✅ Published: {message} to {topic}")

client.disconnect()

#def scheduled_alarm_task():
#  db: Session = SessionLocal()
#  users = db.query(Schedule.user_id).distinct().all()
#
#  for user in users:
#    if user.user_id in online_users:
#      check_and_send_alarms(db, user.user_id)
#
#  db.close()
#
#scheduler = BackgroundScheduler()
#scheduler.add_job(scheduled_alarm_task, 'interval', minutes=1)
#
#def start_scheduler():
#  scheduler.start() if len(online_users) >= 1 else None
#
#start_scheduler