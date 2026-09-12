import paho.mqtt.client as mqtt
from app.service.mqtt_service import On
from app.config.config import MQTTData

class MQTT:
    def __int__(self):
        self.On = On
        
    @staticmethod    
    def on():
        BROKER = MQTTData.BROKER
        PORT = MQTTData.PORT

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        client.username_pw_set(MQTTData.CLIENT_NAME,MQTTData.CLIENT_PASSWORD)

        client.tls_set()

        client.on_connect = On.connect
        client.on_disconnect = On.disconnect
        client.on_message = On.message

        client.connect(BROKER, PORT)

        client.loop_forever()