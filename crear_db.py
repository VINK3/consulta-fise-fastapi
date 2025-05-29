
import json
import sqlite3
import os
import urllib.request

JSON_URL = "https://drive.google.com/file/d/1ojaVYTbouk9L97OQp6d05eKAdwVOA1Bc/view?usp=sharing"
JSON_PATH = "fise.json"
DB_PATH = "datos.db"

def generar_db():
    if not os.path.exists(DB_PATH):
        print("🔄 Descargando JSON...")
        urllib.request.urlretrieve(JSON_URL, JSON_PATH)

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            datos = json.load(f)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                dni TEXT PRIMARY KEY,
                tipo TEXT,
                estado TEXT,
                observacion TEXT
            )
        """)
        for dni, info in datos.items():
            cursor.execute("""
                INSERT OR REPLACE INTO registros (dni, tipo, estado, observacion)
                VALUES (?, ?, ?, ?)
            """, (info["dni"], info["tipo"], info["estado"], info["observacion"]))
        conn.commit()
        conn.close()
        print("✅ Base de datos lista.")
