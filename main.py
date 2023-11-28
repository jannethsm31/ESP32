import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

origins = [
    "",
    "",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("sql/dispositivos.db")

class Datos(BaseModel):
    pot: int
    led: int


@app.post("/actualizar-datos")
async def actualizar_datos(datos: Datos):
    try:
        pot_value = datos.pot
        led_value = datos.led

        c = conn.cursor()
        c.execute('INSERT INTO dispositivos (pot, led) VALUES (?, ?)', (pot_value, led_value))
        conn.commit()

        return {"mensaje": "Datos actualizados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=-1, detail=str(e))

import requests

@app.get("/control-led")
async def control_led():
    try:
        # Lógica para encender o apagar el LED según el estado actual en la base de datos
        c = conn.cursor()
        c.execute('SELECT led FROM dispositivos ORDER BY timestamp DESC LIMIT 1')
        led_value = c.fetchone()[0]

        # Aquí enviamos la señal al ESP32 para controlar el LED
        if led_value == 0:
            # Envía una solicitud HTTP GET para encender el LED en el ESP32
            requests.get("https://esp32-ip/encender-led")
        else:
            # Envía una solicitud HTTP GET para apagar el LED en el ESP32
            requests.get("https://esp32-ip/apagar-led")

        return {"mensaje": f"LED controlado exitosamente a {led_value}"}
    except Exception as e:
        raise HTTPException(status_code=-1, detail=str(e))

@app.get("/obtener-pot")
async def obtener_pot():
    try:
        # Obtener el valor actual del potenciómetro desde la base de datos
        c = conn.cursor()
        c.execute('SELECT pot FROM dispositivos ORDER BY timestamp DESC LIMIT 1')
        pot_value = c.fetchone()[0]

        return {"potenciometro": pot_value}
    except Exception as e:
        raise HTTPException(status_code=-1, detail=str(e))


@app.get("/")
async def bienvenida():
    return {'Desarrollado por': 'Janneth Santos'}