import os
import time

try:
    import paho.mqtt.client as mqtt
except ImportError:
    os.system("cls")
    print("Problema na importação da Biblioteca MQTT")
    time.sleep(5)

BROKER = "" # Coloque o IP DO BROKER.
PORT = "1833" # Coloque a porta que o BROKER está (PADRÃO = 1833)
TOPIC = "" # Coloque o nome do tópico
USERNAME = "grupo1" # Coloque o usuário do Projeto
PASSWORD = "grupo1" # Coloque a senha do Projeto

