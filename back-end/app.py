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
import paho.mqtt.client as mqtt


#                            IMPORT DAS BIBLIOTECAS                                     #
