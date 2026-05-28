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

#                                 CONFIGURAÇÕES INICIAIS                                  #

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/")
async def index(request: Request):
	return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/home")
async def home(request: Request):
	status = request.query_params.get("status", "")
	message = request.query_params.get("message", "")
	return templates.TemplateResponse(
		request,
		"home.html",
		{"request": request, "status": status, "message": message},
	)

@app.get("/input")
async def input(request: Request):
	return templates.TemplateResponse(request, "input.html", {"request": request})

#                                 CONFIGURAÇÕES INICIAIS                                  #

#                                      FORMULARIOS                                        #

def conectar_mqtt(BROKER, PORT, TOPIC, USERNAME, PASSWORD):
	global mqtt_client
	mqtt = importlib.import_module("paho.mqtt.client")
	mqtt_client = mqtt.Client()
	mqtt_client.username_pw_set(USERNAME, PASSWORD)
	mqtt_client.connect(BROKER, PORT)
	mqtt_client.subscribe(TOPIC)
	mqtt_client.loop_start()


def publicar_mqtt(topic, message):
	global mqtt_client
	info = mqtt_client.publish(topic, message)
	info.wait_for_publish()
	if info.rc != 0:
		raise Exception("Falha ao publicar a mensagem no broker MQTT")


@app.post("/formulario")
async def receber_formulario(
	BROKER: Annotated[str, Form()],
	PORT: Annotated[int, Form()],
	TOPIC: Annotated[str, Form()],
	USERNAME: Annotated[str, Form()],
	PASSWORD: Annotated[str, Form()],
):
	try:
		conectar_mqtt(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
		return {"status": "ok"}
	except Exception as e:
		return {"status": "error", "message": str(e)}


@app.post("/led/on")
async def ligar_led():
	try:
		publicar_mqtt("esp32/led", "ON")
		return RedirectResponse(url="/home?status=success&message=LED%20ligado%20e%20mensagem%20enviada%20ao%20broker", status_code=303)
	except Exception as e:
		return RedirectResponse(url="/home?status=error&message=Falha%20ao%20publicar%20no%20broker%20MQTT", status_code=303)


#                                 FORMULÁRIOS                                             #

#                                 FORMULÁRIOS                                             #






