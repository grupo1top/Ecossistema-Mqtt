# 🟩 Ecossistema-MQTT
Este projeto foi desenvolvido com a finalidade de criar um ambiente de comunicação fundamentado no protocolo MQTT, aplicando conceitos de Internet das Coisas (IoT), redes de computadores, sistemas embarcados e desenvolvimento web.

O sistema permite a comunicação entre uma interface web, um broker MQTT e uma ESP32, podendo monitorar o acionamento remoto de um componente físico (LED) conectado ao microcontrolador. 

### 🟩 Objetivo principal

Construir um sistema operacional de troca de dados utilizando MQTT, que é constituído por:

- Broker MQTT rodando no WSL do Windows
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

### 1. Instalar o Mosquitto no WSL

Abra o Ubuntu WSL:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients -y
```

### 2. Configurar o Mosquitto

Edite o arquivo de configuração:

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Apague o conteúdo existente e deixe:

```
pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest stdout

listener 1883

allow_anonymous true
```

Salve:

```
CTRL + O
ENTER
CTRL + X
```

---

### 3. Iniciar o Mosquitto

Execute:

```bash
sudo mosquitto -c /etc/mosquitto/mosquitto.conf -v
```

Se estiver funcionando corretamente aparecerá algo semelhante a:

```
Opening ipv4 listen socket on port 1883.
Opening ipv6 listen socket on port 1883.
```

---

### 4. Verificar se o broker está escutando

Execute:

```bash
sudo ss -tulpn | grep 1883
```

Resultado esperado:

```
tcp LISTEN 0 100 0.0.0.0:1883
```

---

### 5. Descobrir o IP do WSL

Execute:

```bash
hostname -I
```

Exemplo:

```
172.19.40.226
```

Guarde esse IP.

---

### 6. Criar redirecionamento da porta no Windows

Abra o PowerShell como ADMINISTRADOR.

Execute:

```powershell
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=1883 connectaddress=172.19.40.226 connectport=1883
```

Substitua:

```
172.19.40.226
```

pelo IP do seu WSL.

---

### 7. Liberar a porta no Firewall do Windows

No PowerShell Admin:

```powershell
New-NetFirewallRule -DisplayName "MQTT Mosquitto 1883" -Direction Inbound -Protocol TCP -LocalPort 1883 -Action Allow
```

---

### 8. Validar o portproxy

Execute:

```powershell
netsh interface portproxy show all
```

Resultado esperado:

```
0.0.0.0     1883     172.19.40.226     1883
```

---

### 9. Descobrir o IP do Windows

No CMD ou PowerShell:

```powershell
ipconfig
```

Pegue o IPv4 da máquina.

Exemplo:

```
192.168.0.105
```

Esse será o IP utilizado pelos dispositivos externos.

---

### 10. Testar o broker localmente

## Subscriber

Abra um terminal WSL:

```bash
mosquitto_sub -h localhost -t Aula
```

---

## Publisher

Abra outro terminal WSL:

```bash
mosquitto_pub -h localhost -t Aula -m "Teste MQTT"
```

Resultado esperado:

```
Teste MQTT
```

---

### 11. Testar via MQTT Explorer

Instale:

MQTT Explorer

Configure:

```
Host: 192.168.0.105
Port: 1883
SSL/TLS: OFF
Username: vazio
Password: vazio
```

Clique em:

```
CONNECT
```

---

### 12. Publicar mensagens para teste

No WSL:

```bash
mosquitto_pub -h localhost -t Aula -m "Primeira mensagem"
```

No MQTT Explorer aparecerá:

```
Aula
 └── Primeira mensagem
```
#### Subscriber

```
mosquitto_sub -h localhost -t teste
```

#### Publisher

```
mosquitto_pub -h localhost -t teste -m "Olá MQTT"
```

Após o envio da mensagem, o subscriber recebeu os dados corretamente, validando o funcionamento do broker.

### 🟩 Problemas e Soluções Aplicadas na Configuração do Broker MQTT

### 1. Falha na Inicialização do Broker Mosquitto

Problema
O serviço Mosquitto não iniciava corretamente, apresentando o erro:

```bash
Error: Unable to write pid file.
```
Causa
Ausência da pasta necessária para armazenamento do arquivo PID e permissões inadequadas.

Solução

Criação da pasta e ajuste das permissões:

```bash
sudo mkdir -p /run/mosquitto
sudo chown mosquitto:mosquitto /run/mosquitto
```

---

### 2. Conflito na Porta 1883

Problema
Ao iniciar o broker foi exibido o erro:

```bash
Error: Address already in use
```
Causa
A porta 1883 já estava sendo utilizada por outra instância do Mosquitto.

Solução

Verificação dos serviços utilizando a porta:

```bash
sudo ss -tulnp | grep 1883
```

Resultado obtido:

```text
0.0.0.0:1883
```

Confirmando que o broker já estava em execução.

---

### 3. Broker Restrito a Conexões Locais

Problema
O Mosquitto aceitava apenas conexões locais.

Mensagem observada:

```bash
Starting in local only mode.
```

Causa
Configuração padrão do broker.

Solução

Edição do arquivo de configuração:

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

Adição das configurações:

```conf
listener 1883
allow_anonymous true
```

Reinicialização do serviço:

```bash
sudo systemctl restart mosquitto
```

---

### 4. Dispositivos Externos Não Conseguam Acessar o Broker

Problema
Clientes MQTT externos apresentavam erro de conexão.

**Sintoma:**

```text
Connection Lost
```
Causa
O WSL2 opera em modo NAT, impedindo acesso direto ao broker hospedado no Linux.

Solução

Configuração do Port Proxy no Windows para encaminhar o tráfego da porta 1883 para o IP interno do WSL:

```powershell
netsh interface portproxy add v4tov4 `
listenport=1883 `
listenaddress=0.0.0.0 `
connectport=1883 `
connectaddress=IP_DO_WSL
```

---

### 5. Port Proxy Restrito ao Localhost

Problema
O encaminhamento estava aceitando apenas conexões locais.

Verificação realizada:

```powershell
netstat -ano | findstr 1883
```

Resultado encontrado:

```text
TCP 127.0.0.1:1883 0.0.0.0:0 LISTENING
```

Causa
O Port Proxy estava vinculado apenas ao localhost, impedindo conexões externas.

Solução

Remoção das configurações anteriores:

```powershell
netsh interface portproxy reset
```

Reinicialização do serviço responsável:

```powershell
net stop iphlpsvc
net start iphlpsvc
```

Descoberta do IP atual do WSL:

```bash
ip addr show eth0
```

Criação de novo encaminhamento:

```powershell
netsh interface portproxy add v4tov4 listenport=1883 listenaddress=0.0.0.0 connectport=1883 connectaddress=IP_DO_WSL
```

Validação:

```powershell
netstat -ano | findstr 1883
```

Resultado esperado:

```text
TCP 0.0.0.0:1883 0.0.0.0:0 LISTENING
```

---

### 6. Bloqueio da Porta pelo Firewall do Windows

Problema
As conexões externas continuavam falhando.

Causa
A porta 1883 não possuía regra de liberação no firewall.

Solução

Criação da regra:

```powershell
New-NetFirewallRule `
-DisplayName "MQTT1883" `
-Direction Inbound `
-Protocol TCP `
-LocalPort 1883 `
-Action Allow
```

Validação da regra:

```powershell
Get-NetFirewallRule -DisplayName "MQTT1883"
```

Resultado:

```text
Enabled   : True
Action    : Allow
Direction : Inbound
```

Confirmando que a regra foi criada corretamente.

---

### 7. Testes de Conectividade

Problema
Necessidade de verificar se a porta estava acessível pela rede.

Solução

Teste realizado a partir de outro dispositivo:

```powershell
Test-NetConnection 192.168.0.15 -Port 1883
```

Resultado:

```text
TcpTestSucceeded : True
```

Confirmando a acessibilidade da porta.

---

### 8. Erros Durante Testes MQTT

8.1 Publicação sem mensagem

Erro

```bash
Both topic and message must be supplied.
```

Causa
O comando de publicação foi executado sem informar a mensagem.

Solução

Utilização do comando correto:

```bash
mosquitto_pub -h localhost -t Aula -m "oi"
```

---

8.2 Assinatura de tópico aparentemente travada

Problema
O comando permanecia aguardando indefinidamente.

Causa
Comportamento normal do cliente MQTT Subscriber, que permanece escutando mensagens até ser encerrado.

Comando utilizado

```bash
mosquitto_sub -h localhost -t Aula
```

Para interromper a execução:

```bash
CTRL + C
```

---


#### Endereço do Broker
#### 
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
<img width="1600" height="899" alt="WhatsApp Image 2026-06-11 at 10 48 15" src="https://github.com/user-attachments/assets/fa035a56-60a4-46ba-b9e3-162c96fbd87e" />


### 🟩 Vídeos do funcionamento
https://github.com/user-attachments/assets/f3248cd9-5c77-492a-abef-b5cfd8007cdd

https://github.com/user-attachments/assets/2c7f14da-3105-4183-b3fb-e71c3082d2de

https://github.com/user-attachments/assets/c4f1738f-7d17-4852-a098-31364342dcde



