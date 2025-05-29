
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from crear_db import generar_db

app = FastAPI()
generar_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/buscar")
def buscar(dni: str):
    conn = sqlite3.connect("datos.db")
    cur = conn.cursor()
    cur.execute("SELECT dni, tipo, estado, observacion FROM registros WHERE dni = ?", (dni,))
    fila = cur.fetchone()
    conn.close()
    if fila:
        return {
            "dni": fila[0],
            "tipo": fila[1],
            "estado": fila[2],
            "observacion": fila[3]
        }
    else:
        return JSONResponse({"error": "DNI no encontrado"}, status_code=404)
