import json

class On:
    def connect(client, userdata, flags, reason_code, properties):
        print(">>> on_connect foi chamado")
        print("Reason code:", reason_code)

        if reason_code == 0:
            print(">>> CONECTADO!")
            client.subscribe("botao/estado")
        else:
            print(">>> FALHA NA CONEXÃO")

    def disconnect(client, userdata, flags, reason_code, properties):
        print(">>> DESCONECTADO")
        print("Reason code:", reason_code)

    def message(client, userdata, msg):
        men = json.loads(msg.payload.decode())
        print(f"Recebemos o valor: {men["data"]} do dispositivo {men["origem"]}")

