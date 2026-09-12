import json

class On:
    def connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Sistema iniciado")
            client.subscribe("botao/estado")
        else:
            print(f"Conexão falhou, Codigo: {reason_code}")

    def disconnect(client, userdata, flags, reason_code, properties):
        print(f"Conexão perdida Codigo: {reason_code}")

    def message(client, userdata, msg):
        men = json.loads(msg.payload.decode())
        print(f"Recebemos o valor: {men["data"]} do dispositivo {men["origem"]}")

