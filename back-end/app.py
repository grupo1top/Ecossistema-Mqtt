#                            IMPORT DAS BIBLIOTECAS                                     #

import os
import time
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


@app.post("/formulario")
async def receber_formulario(
	BROKER: Annotated[str, Form()],
	PORT: Annotated[int, Form()],
	TOPIC: Annotated[str, Form()],
	USERNAME: Annotated[str, Form()],
	PASSWORD: Annotated[str, Form()],
):
	return {
		"BROKER": BROKER,
		"PORT": PORT,
		"TOPIC": TOPIC,
		"USERNAME": USERNAME,
		"PASSWORD": PASSWORD,
	}


#                                 FORMULÁRIOS                                             #




