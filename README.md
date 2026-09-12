# SISME Bridge

Base de integração entre dispositivos **ESP32** e o sistema SISME. Este
serviço funciona como uma ponte MQTT: recebe as mensagens publicadas pelos
dispositivos, organiza o payload e deixa o caminho preparado para que os dados
sejam encaminhados ao backend da aplicação. Os schemas de validação já estão
definidos, mas sua aplicação no fluxo de recebimento ainda é um próximo passo.

## Visão geral

```text
ESP32  ── MQTT/TLS ──>  SISME Bridge (Python)  ──>  Backend SISME
                              │
                              └── tópico: botao/estado
```

O bridge centraliza a comunicação com o broker MQTT e evita que o backend
precise lidar diretamente com a conexão de cada ESP32. Isso permite adicionar
dispositivos, sensores e regras de encaminhamento sem acoplar o hardware à
implementação interna do sistema.

## Estado atual

Atualmente, o projeto:

- conecta-se a um broker MQTT usando TLS;
- autentica no broker com usuário e senha;
- usa `sisme-bridge` como identificador MQTT padrão;
- assina o tópico `botao/estado` após conectar;
- decodifica as mensagens recebidas como JSON;
- exibe a origem e os dados recebidos no console;
- define schemas Pydantic para mensagens de sensores, alertas e login.

O encaminhamento efetivo para o backend SISME ainda é o próximo ponto de
integração. A variável `SISME_BACKEND_URL` já existe como configuração
reservada para essa etapa.

## Tecnologias

- Python 3.12 ou superior;
- Paho MQTT;
- MQTT sobre TLS;
- Pydantic;
- python-dotenv.

As dependências estão em [`requirements.txt`](./requirements.txt).

## Estrutura do projeto

```text
.
├── app/
│   ├── config/
│   │   └── config.py          # Configurações carregadas do ambiente
│   ├── mqtt/
│   │   └── main.py            # Criação e conexão do cliente MQTT
│   ├── schemas/
│   │   └── payload_schema.py   # Contratos dos payloads
│   ├── service/
│   │   └── mqtt_service.py    # Callbacks de conexão e mensagens
│   └── main.py                # Ponto de entrada da aplicação
├── run.py                     # Inicializa o bridge
├── requirements.txt
└── .env                       # Configuração local; não versionar
```

## Configuração

Crie um arquivo `.env` na raiz do projeto. Nunca publique esse arquivo no
repositório, pois ele contém credenciais do broker.

```env
SISME_MQTT_BROKER=seu-broker-mqtt
SISME_MQTT_PORT=8883
SISME_MQTT_USERNAME=seu-usuario
SISME_MQTT_PASSWORD=sua-senha
SISME_MQTT_CLIENT_ID=sisme-bridge
SISME_BACKEND_URL=http://localhost:1000
```

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `SISME_MQTT_BROKER` | Sim | Hostname do broker MQTT. |
| `SISME_MQTT_PORT` | Não | Porta MQTT. O padrão é `8883` para MQTT/TLS. |
| `SISME_MQTT_USERNAME` | Sim | Usuário de autenticação no broker. |
| `SISME_MQTT_PASSWORD` | Sim | Senha de autenticação no broker. |
| `SISME_MQTT_CLIENT_ID` | Não | ID do cliente MQTT. O padrão é `sisme-bridge`. |
| `SISME_BACKEND_URL` | Não | URL reservada para a integração com o backend SISME. |

Se as credenciais que estão ou estiveram no `.env` já foram compartilhadas,
faça a rotação delas no broker e atualize o arquivo local.

## Instalação

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se a política de execução do PowerShell impedir a ativação do ambiente,
execute o Python diretamente pelo caminho `venv\Scripts\python.exe`.

## Execução

Com o ambiente virtual ativado:

```powershell
python run.py
```

Ao iniciar corretamente, o processo mantém a conexão aberta com
`loop_forever()`. Quando uma mensagem chega ao tópico assinado, o bridge
imprime no console os campos `data` e `origem`.

Para interromper a execução, use `Ctrl+C`.

## Contrato de mensagens

As mensagens devem ser publicadas como JSON. O campo `origem` identifica o
ESP32 ou dispositivo de origem, `datatype` identifica o tipo de mensagem e
`data` contém o conteúdo específico.

### Sensores

```json
{
  "origem": "esp32-pulseira-01",
  "datatype": "sensores",
  "data": {
    "bpm": 72,
    "spo2": 98,
    "bateria": 87
  }
}
```

Regras dos campos:

- `bpm`: entre `0` e `300`;
- `spo2`: entre `0` e `100`;
- `bateria`: entre `0` e `100`.

### Alerta

```json
{
  "origem": "esp32-pulseira-01",
  "datatype": "alerta",
  "data": {
    "tipo": "queda",
    "mensagem": "Possível queda detectada"
  }
}
```

## Integração com o ESP32

### Firmware de referência

O firmware utilizado como referência para esta ponte está disponível no
repositório [MarcoosDev/ESP32-MQTT](https://github.com/MarcoosDev/ESP32-MQTT).
Ele foi desenvolvido para a placa **ESP32-C3 DevKitM-1**, usando o framework
Arduino e o PlatformIO.

Esse projeto já fornece a base necessária para a comunicação com o bridge:

- conexão e manutenção da rede Wi-Fi;
- conexão autenticada com o broker MQTT;
- comunicação MQTT protegida por TLS/SSL;
- publicação e assinatura de tópicos MQTT;
- payloads em formato JSON;
- reconexão automática quando o Wi-Fi ou o broker ficam indisponíveis;
- certificado CA configurado para validar o broker;
- monitor serial em `115200` para acompanhamento da comunicação.

No firmware, a lógica está organizada principalmente da seguinte forma:

| Componente | Responsabilidade |
| --- | --- |
| `main.cpp` | Inicializa a serial, o Wi-Fi, o cliente MQTT e os callbacks. |
| `wifi.cpp` | Conecta o ESP32 à rede e mantém a conexão ativa. |
| `mqtt.cpp` | Gerencia a conexão MQTT e a inscrição em tópicos. |
| `conexoes.cpp` | Coordena as tentativas de reconexão. |
| `config.cpp` | Concentra credenciais e parâmetros de rede e do broker. |
| `json.cpp` | Monta os payloads JSON publicados pelo dispositivo. |

O firmware do ESP32 deve:

1. conectar-se à rede Wi-Fi;
2. conectar-se ao mesmo broker MQTT usando TLS;
3. autenticar com as credenciais autorizadas;
4. publicar os payloads JSON no tópico `botao/estado`;
5. usar um valor estável e identificável em `origem`;
6. implementar reconexão e reenvio conforme a necessidade do projeto.

Para configurar o firmware, os parâmetros `mqtt_server`, `mqtt_port`,
`mqtt_user`, `mqtt_pass`, `client_id` e `ca_cert` devem apontar para o mesmo
ambiente utilizado pelas variáveis `SISME_MQTT_*` deste projeto. O certificado
CA usado pelo ESP32 deve validar o broker configurado no bridge.

O broker deve permitir que o usuário do bridge assine o tópico e que os
dispositivos publiquem nele. Em ambientes com vários tipos de mensagem, os
tópicos podem ser separados posteriormente, por exemplo:

```text
sisme/{dispositivo}/sensores
sisme/{dispositivo}/alertas
```

Essa organização é uma evolução possível; o tópico atualmente utilizado pelo
código é `botao/estado`.

## Próximos passos sugeridos

- validar os payloads recebidos com `PayloadSchema` antes do processamento;
- encaminhar sensores, alertas e logins para endpoints do backend SISME;
- definir tópicos e permissões por dispositivo;
- adicionar logs estruturados e tratamento de mensagens inválidas;
- implementar reconexão com backoff e monitoramento da conexão;
- adicionar testes para os contratos de payload e para os callbacks MQTT;
- documentar o contrato definitivo entre o firmware ESP32, o bridge e o
  backend.

## Segurança

- não versione `.env`, certificados ou credenciais;
- use MQTT sobre TLS e valide os certificados do broker;
- forneça permissões mínimas para cada cliente MQTT;
- atribua um `CLIENT_ID` único quando houver múltiplas instâncias do bridge;
- não registre senhas ou tokens nos logs;
- rotacione credenciais que tenham sido expostas.

As credenciais e o certificado CA do firmware também devem permanecer fora de
repositórios públicos. Consulte o
[README do projeto ESP32-MQTT](https://github.com/MarcoosDev/ESP32-MQTT) para
as instruções de compilação, upload e configuração da placa.
