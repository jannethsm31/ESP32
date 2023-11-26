import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

conn = sqlite3.connect("sql/datos.db")

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

class iot(BaseModel):
    valor: str

@app.get("/led")
async def obtener_estado_led():
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM dispositivos')
        response = [{'valor': row[2]} for row in c]
        return response
    except Exception as e:
        raise HTTPException(status_code=-1, detail=str(e))

@app.post("/led/{estado}")
async def cambiar_estado_led(estado: int):
    try:
        if estado not in [0, 1]:
            raise HTTPException(status_code=-1, detail="El estado debe ser 0 o 1")

        c = conn.cursor()
        c.execute('INSERT INTO dispositivos (valor) VALUES (?)', (str(estado),))
        conn.commit()

        # Lógica para controlar el LED según el estado


        return {"mensaje": f"Estado del LED cambiado exitosamente a {estado}"}
    except Exception as e:
        raise HTTPException(status_code=-1, detail=str(e))

@app.get("/")
async def bienvenida():
    return {'Desarrollado por': 'Janneth Santos'}
