import socket
import threading
import sqlite3
import json
import queue
from concurrent.futures import ThreadPoolExecutor
 
HOST = "127.0.0.1"
PUERTO = 6000
CANTIDAD_WORKERS = 4
DB_PATH = "tareas_distribuidas.db"

lock_db = threading.Lock()
 
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
 
 
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo    TEXT    NOT NULL,
                completa  INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

cola_tareas = queue.Queue()
pool_workers = ThreadPoolExecutor(max_workers=CANTIDAD_WORKERS, thread_name_prefix="worker")
 
 
def procesar_tarea(pedido):
    accion = pedido.get("accion")
 
    with lock_db:
        with get_db() as conn:
            if accion == "crear":
                titulo = (pedido.get("titulo") or "").strip()
                if not titulo:
                    return {"ok": False, "error": "El titulo es obligatorio"}
                cur = conn.execute(
                    "INSERT INTO tareas (titulo) VALUES (?)", (titulo,)
                )
                conn.commit()
                return {"ok": True, "resultado": {"id": cur.lastrowid, "titulo": titulo}}
 
            elif accion == "listar":
                filas = conn.execute(
                    "SELECT id, titulo, completa FROM tareas ORDER BY id"
                ).fetchall()
                tareas = [dict(f) for f in filas]
                return {"ok": True, "resultado": tareas}
 
            elif accion == "completar":
                id_tarea = pedido.get("id")
                cur = conn.execute(
                    "UPDATE tareas SET completa = 1 WHERE id = ?", (id_tarea,)
                )
                conn.commit()
                if cur.rowcount == 0:
                    return {"ok": False, "error": f"No existe la tarea {id_tarea}"}
                return {"ok": True, "resultado": f"Tarea {id_tarea} marcada como completa"}
 
            else:
                return {"ok": False, "error": f"Accion desconocida: {accion}"}
 
 
def despachador():
    while True:
        pedido, conexion_cliente = cola_tareas.get()
        futuro = pool_workers.submit(procesar_tarea, pedido)
        futuro.add_done_callback(lambda f, conn=conexion_cliente: enviar_respuesta(conn, f.result()))
 
 
def enviar_respuesta(conexion_cliente, respuesta):
    try:
        conexion_cliente.sendall((json.dumps(respuesta) + "\n").encode())
    except OSError:
        pass
 
def atender_cliente(conexion, direccion):
    print(f"[+] Conexión entrante de {direccion}")
    buffer = ""
    try:
        with conexion:
            while True:
                datos = conexion.recv(4096)
                if not datos:
                    break
                buffer += datos.decode()
 
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    if not linea.strip():
                        continue
                    try:
                        pedido = json.loads(linea)
                    except json.JSONDecodeError:
                        enviar_respuesta(conexion, {"ok": False, "error": "JSON inválido"})
                        continue

                    cola_tareas.put((pedido, conexion))
    except ConnectionResetError:
        pass
    finally:
        print(f"[-] Conexión cerrada de {direccion}")
 
 
def main():
    init_db()
 
    hilo_despachador = threading.Thread(target=despachador, daemon=True)
    hilo_despachador.start()
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen()
        print(f"Servidor escuchando en {HOST}:{PUERTO} con {CANTIDAD_WORKERS} workers")
 
        while True:
            conexion, direccion = servidor.accept()
            hilo_cliente = threading.Thread(
                target=atender_cliente, args=(conexion, direccion), daemon=True
            )
            hilo_cliente.start()
 
 
if __name__ == "__main__":
    main()
 