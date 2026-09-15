import os
from dotenv import load_dotenv

load_dotenv()

class MQTTData:
    BROKER = os.getenv("SISME_MQTT_BROKER")
    PORT = int(os.getenv("SISME_MQTT_PORT", 8883))
    CLIENT_NAME = os.getenv("SISME_MQTT_USERNAME")
    CLIENT_PASSWORD = os.getenv("SISME_MQTT_PASSWORD")
    CLIENT_ID = os.getenv("SISME_MQTT_CLIENT_ID", "sisme-bridge")

class SISMEData:
    URL = os.getenv("SISME_BACKEND_URL")