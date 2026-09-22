import socket
from constantes import HOST, PORT, COMANDO_SALIDA

# Conectar al servidor
def conectar():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PORT))
        print(f"Conectado al servidor {HOST}:{PORT}\n")
        return cliente
    except ConnectionRefusedError:
        print("No se pudo conectar. ¿Está corriendo el servidor?")
        return None


# Enviar mensajes hasta escribir la palabra de salida
def enviar_mensajes(cliente):
    print(f"Escribí mensajes ('{COMANDO_SALIDA}' para salir):\n")
    while True:
        mensaje = input("Vos: ")

        cliente.sendall(mensaje.encode("utf-8"))
        respuesta = cliente.recv(1024).decode("utf-8")
        print(f"Servidor: {respuesta}\n")

        if mensaje.lower() == COMANDO_SALIDA.lower():
            break


# --- Programa principal ---
if __name__ == "__main__":
    cliente = conectar()
    if cliente:
        enviar_mensajes(cliente)
        cliente.close()
        print("Conexión cerrada.")