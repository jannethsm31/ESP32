import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

conn = sqlite3.connect("sql/dispositivos.db")

app = FastAPI()

origins = [
    "https://wokwi.com/projects/382288042107508737",
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
        dispositivo = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
        response.append(dispositivo)
    return response

# Dispositivos por id
@app.get("/dispositivos/{id}")
async def dispositivos(id: str):
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos WHERE id = ?', (id,))
    dispositivo = None
    for row in c:
        dispositivo = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
    return dispositivo

@app.put("/dispositivos/{id}")
async def actualizar_dispositivo(id: str, dispositivo: Datos):
    """Actualiza un dispositivo."""
    c = conn.cursor()
    c.execute('UPDATE dispositivos SET dispositivo = ?, valor = ? WHERE id = ?',
              (dispositivo.pot, dispositivo.valor, id))
    conn.commit()
    return dispositivo
