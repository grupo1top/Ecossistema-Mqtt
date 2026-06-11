# 🟩 Ecossistema-Mqtt
Este projeto foi desenvolvido com a finalidade de criar um ambiente de comunicação fundamentado no protocolo MQTT, aplicando conceitos de Internet das Coisas (IoT), redes de computadores, sistemas embarcados e desenvolvimento web.

O sistema permite a comunicação entre uma interface web, um broker MQTT e uma ESP32, podendo monitorar o acionamento remoto de um componente físico (LED) conectado ao microcontrolador. 

### 🟩 Objetivo principal

Construir um sistema operacional de troca de dados utilizando MQTT, que é constituído por:

- Corretor MQTT rodando no WSL do Windows
- ESP32 que se conecta ao corretor
- Interface web para monitoramento e controle
- Ativação de um componente físico (LED foi o escolhido)

### 🟩 Tecnologias utilizada

Hardware

- ESP32
- LED
- Jumpers
- Protoboard
- Resistor

Software

- WSL
- Mosquitto MQTT Broker
- Visual Studio Code
- Programação em Python + HTML + CSS + Java
- FastAPI + venv
- Jinja2 Templates (renderização HTML)
- Paho MQTT (cliente MQTT em Python)

### 🟩 Funcionamento

O funcionamento do sistema ocorre por meio da comunicação entre o broker MQTT, a ESP32 e a aplicação web. O broker MQTT é executado dentro do WSL utilizando o Mosquitto, sendo responsável pelo gerenciamento da troca de mensagens entre os dispositivos conectados. A ESP32 é conectada ao broker através da rede Wi-Fi, permitindo o envio e recebimento de informações em tempo real. O sistema web é responsável por enviar comandos MQTT para tópicos específicos, possibilitando o acionamento do dispositivo conectado à ESP32. No sistema desenvolvido, é possível ligar, desligar ou fazer o LED piscar por meio da interface web. Ao receber as mensagens MQTT, a ESP32 interpreta os comandos enviados e executa a ação correspondente. Após a execução da ação, o estado atual do dispositivo é enviado novamente ao broker MQTT, permitindo que o sistema web monitore e exiba o status do equipamento ao usuário, garantindo o acompanhamento do funcionamento do componente físico conectado à ESP32.


### 🟩 Configurações realizadas

Para instalação e configuração principal do mosquitto fizemos as seguintes configurações:

#### Atualização do sistema

```
sudo apt update
sudo apt upgrade
```

#### Instalação do Mosquitto

```
sudo apt install mosquitto
sudo apt install mosquitto-clients
```

#### Inicialização do serviço

```
sudo systemctl start mosquitto
```

#### Verificação do status

```
sudo systemctl status mosquitto
```

Para validar o funcionamento do broker foram realizados testes de publicação e subscrição utilizando terminal Linux.

#### Subscriber

```
mosquitto_sub -h localhost -t teste
```

#### Publisher

```
mosquitto_pub -h localhost -t teste -m "Olá MQTT"
```

Após o envio da mensagem, o subscriber recebeu os dados corretamente, validando o funcionamento do broker.

#### Endereço do Broker
#### 

IP utilizado:

```
[192.168.0.72]
```

Porta padrão MQTT:
```
1883
```
A ESP32 foi configurada para conectar-se à rede Wi-Fi e ao broker MQTT. Após a conexão, o dispositivo ficou responsável por:

- Receber comandos MQTT;
- Acionar um LED/dispositivo físico;
- Enviar informações de status ao sistema.
- Funcionamento

Quando o sistema web envia o comando:

ON

A ESP32 liga o dispositivo.

Quando o sistema envia:

OFF

A ESP32 desliga o dispositivo.

Quando o sistema web envia o comando:

BLINK

A ESP32 pisca o LED

### 🟩 Estrutura dos Tópicos MQTT

Os tópicos MQTT foram organizados para permitir a comunicação entre o sistema web e a ESP32, sendo utilizados para o envio de comandos ao LED conectado ao microcontrolador.

| Função | Tópico | Mensagem |
| --- | --- | --- |
| Ligar LED | `esp32/led` | `ON` |
| Desligar LED | `esp32/led` | `OFF` |
| Piscar LED | `esp32/led` | `BLINK` |

O sistema web publica mensagens no tópico `esp32/led`, permitindo que a ESP32 interprete o comando recebido e execute a ação correspondente no componente físico.

### 🟩 Instruções para Execução do Projeto

Para executar o projeto corretamente, é necessário configurar o broker MQTT, iniciar o sistema web e conectar a ESP32 ao broker.

#### 1. Instalar as dependências do projeto

Primeiramente, instale as bibliotecas necessárias do Python:

```bash
pip install fastapi jinja2 python-multipart paho-mqtt
```

Caso exista um arquivo `requirements.txt`, utilize:

```bash
pip install -r requirements.txt
```

#### 2. Iniciar o broker MQTT (Mosquitto)

No WSL, execute os comandos abaixo para iniciar o Mosquitto:

```bash
sudo systemctl start mosquitto
```

Para verificar se o broker está em funcionamento:

```bash
sudo systemctl status mosquitto
```

O broker deverá estar disponível no IP configurado pela rede local utilizando a porta padrão `1883`.

#### 3. Executar o sistema web

No terminal do projeto, execute o arquivo principal do sistema:

```
python app.py
```

Após a inicialização, o sistema poderá ser acessado pelo navegador através do endereço configurado no projeto.

#### 4. Configurar a conexão MQTT no sistema

Ao abrir a aplicação, informe os dados do broker MQTT:

- **Broker/IP:** endereço IP do broker MQTT;
- **Porta:** `1883`;
- **Tópico MQTT:** `esp32/led`;
- **Usuário e senha:** caso configurados no broker.

Após preencher os dados, realize a conexão com o broker.

#### 5. Executar a ESP32

Faça o upload do código para a ESP32 através da Arduino IDE e conecte-a à mesma rede Wi-Fi do broker MQTT.

Após a conexão, a ESP32 ficará apta a receber comandos MQTT enviados pelo sistema web.

#### 6. Testar o acionamento do LED

Na interface web, utilize os botões disponíveis para:

- **Ligar LED** (`ON`);
- **Desligar LED** (`OFF`);
- **Piscar LED** (`BLINK`).

Ao selecionar uma das opções, a mensagem será enviada ao broker MQTT e interpretada pela ESP32, executando a ação correspondente no dispositivo físico.

### 🟩 Fotos do funcionamento
<img width="1600" height="900" alt="WhatsApp Image 2026-05-28 at 07 57 58" src="https://github.com/user-attachments/assets/a97d7d62-c95e-4345-87d0-3d65835aa195" />
<img width="1280" height="720" alt="WhatsApp Image 2026-05-28 at 19 31 14" src="https://github.com/user-attachments/assets/ebe00883-1383-42e4-92dd-c4898be230c5" />

### 🟩 Vídeos do funcionamento
https://github.com/user-attachments/assets/f3248cd9-5c77-492a-abef-b5cfd8007cdd

https://github.com/user-attachments/assets/2c7f14da-3105-4183-b3fb-e71c3082d2de

https://github.com/user-attachments/assets/c4f1738f-7d17-4852-a098-31364342dcde



