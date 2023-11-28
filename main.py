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


@app.get("/")
async def bienvenida():
    return {'Desarrollado por': 'Janneth Santos'}
