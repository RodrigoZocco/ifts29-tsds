import socket
import threading
from constantes import HOST, PORT
from db import inicializar_db, guardar_mensaje

# Recibe y responde los mensajes de un cliente (corre en su propio hilo)
def manejar_cliente(conn, addr):
    print(f"Cliente conectado: {addr[0]}")
    while True:
        datos = conn.recv(1024)
        if not datos:
            break

        mensaje = datos.decode("utf-8")
        print(f"[{addr[0]}] {mensaje}")

        # Guardar en la DB y obtener el timestamp
        timestamp = guardar_mensaje(mensaje, addr[0])

        # Responder al cliente con el timestamp
        respuesta = f"Mensaje recibido: {timestamp}"
        conn.sendall(respuesta.encode("utf-8"))

    conn.close()
    print(f"Cliente {addr[0]} desconectado.")


# Configuración del socket TCP/IP
def inicializar_socket():
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen(5)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        return servidor
    except OSError:
        print(f"Error: el puerto {PORT} ya está en uso.")
        return None


# Aceptar conexiones e iniciar 1 hilo por cada cliente
# Aca en la linea de accept, se queda esperando hasta que se conecta un cliente
# y ahi crea el hilo y lo inicia para manejar ese cliente
def aceptar_conexiones(servidor):
    print("Esperando clientes...\n")
    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()


# --- Programa principal ---
if __name__ == "__main__":
    inicializar_db()
    servidor = inicializar_socket()

    if servidor:
        try:
            aceptar_conexiones(servidor)
        except KeyboardInterrupt:
            print("Servidor detenido")
        finally:
            servidor.close()