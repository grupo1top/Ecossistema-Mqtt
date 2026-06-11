#                            IMPORT DAS BIBLIOTECAS                                     #

import os
import time
import importlib
from threading import Lock
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
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

mqtt_client = None
mqtt_lock = Lock()
mqtt_topic = ""
COMMAND_TOPIC = "esp32/led"
mqtt_state = {
	"connected": False,
	"subscribed": False,
	"broker": "",
	"port": None,
	"topic": "",
	"subscribed_topics": [],
	"state": "Aguardando conexão",
	"last_message": "",
	"last_message_topic": "",
	"updated_at": "",
}


def obter_estado_mqtt():
	with mqtt_lock:
		return dict(mqtt_state)


def atualizar_estado_mqtt(topic, payload):
	normalized = payload.strip().upper()
	if normalized in {"ON", "1", "LIGADO"}:
		state = "LIGADO"
	elif normalized in {"OFF", "0", "DESLIGADO"}:
		state = "DESLIGADO"
	elif normalized in {"BLINK", "PISCAR"}:
		state = "PISCANDO"
	else:
		state = f"Mensagem recebida: {payload}"

	with mqtt_lock:
		mqtt_state["state"] = state
		mqtt_state["last_message_topic"] = topic
		mqtt_state["last_message"] = payload
		mqtt_state["updated_at"] = time.strftime("%d/%m/%Y %H:%M:%S")


def obter_topicos_subscribe():
	topics = []
	for topic in (mqtt_topic, COMMAND_TOPIC):
		if topic and topic not in topics:
			topics.append(topic)
	return topics


def mqtt_on_connect(client, userdata, flags, rc, properties=None):
	with mqtt_lock:
		mqtt_state["connected"] = rc == 0
		mqtt_state["updated_at"] = time.strftime("%d/%m/%Y %H:%M:%S")
	if rc == 0:
		topics = obter_topicos_subscribe()
		for topic in topics:
			client.subscribe(topic)
		with mqtt_lock:
			mqtt_state["subscribed"] = bool(topics)
			mqtt_state["subscribed_topics"] = topics
			if topics:
				mqtt_state["state"] = "Inscrito no topico MQTT"
	else:
		with mqtt_lock:
			mqtt_state["subscribed"] = False
			mqtt_state["subscribed_topics"] = []


def mqtt_on_disconnect(client, userdata, *args):
	with mqtt_lock:
		mqtt_state["connected"] = False
		mqtt_state["subscribed"] = False
		mqtt_state["state"] = "Desconectado do broker"
		mqtt_state["updated_at"] = time.strftime("%d/%m/%Y %H:%M:%S")


def mqtt_on_message(client, userdata, msg):
	payload = msg.payload.decode("utf-8", errors="ignore")
	atualizar_estado_mqtt(msg.topic, payload)


def garantir_subscribe_mqtt():
	if mqtt_client is None or not obter_estado_mqtt()["connected"]:
		return

	topics = obter_topicos_subscribe()
	for topic in topics:
		mqtt_client.subscribe(topic)

	with mqtt_lock:
		mqtt_state["subscribed"] = bool(topics)
		mqtt_state["subscribed_topics"] = topics


@app.get("/")
async def index(request: Request):
	return templates.TemplateResponse(request, "index.html", {"request": request})

@app.get("/home")
async def home(request: Request):
	status = request.query_params.get("status", "")
	message = request.query_params.get("message", "")
	mqtt_status = obter_estado_mqtt()
	return templates.TemplateResponse(
		request,
		"home.html",
		{"request": request, "status": status, "message": message, "mqtt_status": mqtt_status},
	)

@app.get("/input")
async def input(request: Request):
	return templates.TemplateResponse(request, "input.html", {"request": request})


#                                 CONFIGURAÇÕES INICIAIS                                  #

#                                      FORMULARIOS                                        #

def conectar_mqtt(BROKER, PORT, TOPIC, USERNAME, PASSWORD):
	global mqtt_client, mqtt_topic
	mqtt = importlib.import_module("paho.mqtt.client")
	if mqtt_client is not None:
		try:
			mqtt_client.loop_stop()
			mqtt_client.disconnect()
		except Exception:
			pass
	mqtt_topic = TOPIC
	callback_api_version = getattr(mqtt, "CallbackAPIVersion", None)
	if callback_api_version is None:
		mqtt_client = mqtt.Client()
	else:
		mqtt_client = mqtt.Client(callback_api_version.VERSION1)
	mqtt_client.on_connect = mqtt_on_connect
	mqtt_client.on_disconnect = mqtt_on_disconnect
	mqtt_client.on_message = mqtt_on_message
	mqtt_client.username_pw_set(USERNAME, PASSWORD)
	with mqtt_lock:
		mqtt_state["connected"] = False
		mqtt_state["subscribed"] = False
		mqtt_state["broker"] = BROKER
		mqtt_state["port"] = PORT
		mqtt_state["topic"] = TOPIC
		mqtt_state["subscribed_topics"] = []
		mqtt_state["state"] = "Conectando ao broker"
		mqtt_state["last_message"] = ""
		mqtt_state["last_message_topic"] = ""
		mqtt_state["updated_at"] = time.strftime("%d/%m/%Y %H:%M:%S")
	rc = mqtt_client.connect(BROKER, PORT)
	if rc != 0:
		with mqtt_lock:
			mqtt_state["connected"] = False
			mqtt_state["state"] = f"Falha ao conectar ao broker (rc={rc})"
			mqtt_state["updated_at"] = time.strftime("%d/%m/%Y %H:%M:%S")
		raise Exception(f"Falha ao conectar ao broker MQTT (rc={rc})")
	mqtt_client.loop_start()


def publicar_mqtt(topic, message):
	global mqtt_client
	if mqtt_client is None:
		raise Exception("Conecte-se ao broker MQTT antes de publicar mensagens")
	if not obter_estado_mqtt()["connected"]:
		raise Exception("Broker MQTT ainda não está conectado")
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


@app.get("/mqtt/status")
async def mqtt_status():
	garantir_subscribe_mqtt()
	return JSONResponse(content=obter_estado_mqtt())




#                                 FORMULÁRIOS                                             #

#                                BOTÕES DA HOME                                           #

@app.post("/led/on")
async def ligar_led():
	try:
		publicar_mqtt(COMMAND_TOPIC, "ON")
		return RedirectResponse(url="/home?status=success&message=LED%20ligado%20e%20mensagem%20enviada%20ao%20broker", status_code=303)
	except Exception as e:
		return RedirectResponse(url="/home?status=error&message=Falha%20ao%20publicar%20no%20broker%20MQTT", status_code=303)


@app.post("/ON")
async def input_ligar():
	try:
		publicar_mqtt(COMMAND_TOPIC, "ON")
		return RedirectResponse(url="/input", status_code=303)
	except Exception as e:
		return RedirectResponse(url="/input", status_code=303)


@app.post("/OFF")
async def input_desligar():
	try:
		publicar_mqtt(COMMAND_TOPIC, "OFF")
		return RedirectResponse(url="/input", status_code=303)
	except Exception as e:
		return RedirectResponse(url="/input", status_code=303)

@app.post("/led/off")
async def desligar_led():
	try:
		publicar_mqtt(COMMAND_TOPIC, "OFF")
		return RedirectResponse(url="/home?status=success&message=LED%20ligado%20e%20mensagem%20enviada%20ao%20broker", status_code=303)
	except Exception as e:
		return RedirectResponse(url="/home?status=error&message=Falha%20ao%20publicar%20no%20broker%20MQTT", status_code=303)
	

@app.post("/led/piscar")
async def piscar_led():
	try:
		publicar_mqtt(COMMAND_TOPIC, "BLINK")
		return RedirectResponse(url="/home?status=success&message=LED%20ligado%20e%20mensagem%20enviada%20ao%20broker", status_code=303)
	except Exception as e:
		return RedirectResponse(url="/home?status=error&message=Falha%20ao%20publicar%20no%20broker%20MQTT", status_code=303)

#                                BOTÕES DA HOME                                           #

