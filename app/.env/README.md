Download MQTT broker:
https://mosquitto.org/download/

Open your terminal in the src/app/ directory and run the following command:
ionic g page login
ionic g page signup
ionic g service services/websocket
ionic g guard auth

Run this command in MySQL:
CREATE DATABASE if NOT EXISTS mediqnect;

Open your terminal in the project directory and run the following command:
npm install axios
npm install mqtt

Open your command prompt and run the following command:
pip install fastapi
pip install paho-mqtt
pip install passlib[bcrypt]
pip install plyer
pip install playsound
pip install pyjwt
pip install pymysql
pip install sqlalchemy
pip install uvicorn

Run the ionic app: ionic serve
Run the fastapi backend: uvicorn main:app --reload

verify /protected: curl -H "Authorization: Bearer <your-token>" http://localhost:8000/protected