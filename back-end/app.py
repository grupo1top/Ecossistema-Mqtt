#                            IMPORT DAS BIBLIOTECAS                                     #

import os
import time

try:
    import paho.mqtt.client as mqtt

except ImportError:
    os.system("cls")
    print("Problema na importação da Biblioteca MQTT")
    time.sleep(5)

#                            IMPORT DAS BIBLIOTECAS                                     #
