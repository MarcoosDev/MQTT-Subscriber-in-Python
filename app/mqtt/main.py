import paho.mqtt.client as mqtt
from app.service.mqtt_service import On
from app.config.mqtt_data import MQQTData

class MQTT:
    def __int__(self):
        self.On = On
        
    @staticmethod    
    def init():
        BROKER = MQQTData.BROKER
        PORT = MQQTData.PORT

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        client.username_pw_set(MQQTData.CLIENT_NAME,MQQTData.CLIENT_PASSWORD)

        client.tls_set()

        client.on_connect = On.connect
        client.on_disconnect = On.disconnect
        client.on_message = On.message

        client.connect(BROKER, PORT)

        client.loop_forever()