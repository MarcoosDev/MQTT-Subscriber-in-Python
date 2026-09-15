import paho.mqtt.client as mqtt
from app.service.mqtt_service import On
from app.config.config import MQTTData

class MQTT:
    def __int__(self):
        self.On = On
        self.client : mqtt.Client

    def on(self):
        BROKER = MQTTData.BROKER
        PORT = MQTTData.PORT

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self.client.username_pw_set(MQTTData.CLIENT_NAME,MQTTData.CLIENT_PASSWORD)

        self.client.tls_set()

        self.client.on_connect = On.connect
        self.client.on_disconnect = On.disconnect
        self.client.on_message = On.message

        self.client.connect(BROKER, PORT)

        self.client.loop_forever()

    def off(self):
        self.client.disconnect()

Mqtt = MQTT()