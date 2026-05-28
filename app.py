#                            IMPORT DAS BIBLIOTECAS                                     #

import os
import time
import importlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi.staticfiles import StaticFiles


#                            IMPORT DAS BIBLIOTECAS                                       #

#                                 FORMULÁRIOS                                             #

app = FastAPI()


def conectar_mqtt(BROKER, PORT, TOPIC, USERNAME, PASSWORD):
	global mqtt_client
	mqtt = importlib.import_module("paho.mqtt.client")
	mqtt_client = mqtt.Client()
	mqtt_client.username_pw_set(USERNAME, PASSWORD)
	mqtt_client.connect(BROKER, PORT)
	mqtt_client.subscribe(TOPIC)
	mqtt_client.loop_start()


@app.post("/formulario")
async def receber_formulario(
	BROKER: Annotated[str, Form()],
	PORT: Annotated[int, Form()],
	TOPIC: Annotated[str, Form()],
	USERNAME: Annotated[str, Form()],
	PASSWORD: Annotated[str, Form()],
):
	conectar_mqtt(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
	return



#                                 FORMULÁRIOS                                             #




