import sqlite3
from datetime import datetime
from constantes import DB_NAME

# Todo lo relacionado a la Base de datos sqlite está aca

# crear la tabla si no existe
def inicializar_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido   TEXT,
                fecha_envio TEXT,
                ip_cliente  TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("Base de datos lista.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la DB: {e}")
        raise


# guardar un mensaje y devuelve el timestamp
# solo devuelvo esto porque en la consigna lo pide para responderle al cliente
def guardar_mensaje(contenido, ip_cliente):
    try:
        conn = sqlite3.connect(DB_NAME)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
            (contenido, fecha, ip_cliente)
        )
        conn.commit()
        conn.close()
        return fecha
    except sqlite3.Error as e:
        print(f"Error al guardar mensaje: {e}")
        return None