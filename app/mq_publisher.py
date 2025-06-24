import paho.mqtt.client as mqtt

# HiveMQ Cloud details
BROKER = '226d38fc646f4e549353211b488ed337.s1.eu.hivemq.cloud'
PORT = 8883
USERNAME = 'esp32'
PASSWORD = 'Mediqnect-2025'

def publish_message(message: str, topic: str):
  client = mqtt.Client()
  client.username_pw_set(USERNAME, PASSWORD)
  client.tls_set()

  try:
    client.connect(BROKER, PORT)
    client.publish(topic, message)
    client.disconnect()
    print(f"Published message: '{message}' to topic: '{topic}'")
  except Exception as e:
    print(f'MQTT publish failed: {e}')
