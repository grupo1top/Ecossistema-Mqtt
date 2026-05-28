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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="css")


@app.get("/")
async def index(request: Request):
	return templates.TemplateResponse(request, "index.html", {"request": request})


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
	try:
		conectar_mqtt(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
		return {"status": "ok"}
	except Exception as e:
		return {"status": "error", "message": str(e)}


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"request": request})



#                                 FORMULÁRIOS                                             #




