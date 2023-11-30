import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

conn = sqlite3.connect("sql/dispositivos.db")

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


class Datos(BaseModel):
    id: str
    pot: str
    led: str

@app.get("/")
async def bienvenida():
    return {'Desarrollado por': 'Janneth Santos'}

# Todos los dispositivos
@app.post("/dispositivos")
async def dispositivos():

        c = conn.cursor()
        c.execute('SELECT * FROM dispositivos')
        response = []
        for row in c:
            dispositivos = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
            response.appende(dispositivo)
        return response

@app.post("/control-led")
async def control_led():
    try:
        c = conn.cursor()
        c.execute('SELECT led FROM dispositivos ORDER BY ')



