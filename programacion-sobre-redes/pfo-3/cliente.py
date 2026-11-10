import socket
import json
 
HOST = "127.0.0.1"
PUERTO = 6000
 
 
def enviar_pedido(pedido):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PUERTO))
        s.sendall((json.dumps(pedido) + "\n").encode())
 
        buffer = ""
        while "\n" not in buffer:
            datos = s.recv(4096)
            if not datos:
                break
            buffer += datos.decode()
 
        linea, _, _ = buffer.partition("\n")
        return json.loads(linea)
 
def crear_tarea():
    titulo = input("Título de la tarea: ").strip()
    respuesta = enviar_pedido({"accion": "crear", "titulo": titulo})
 
    if respuesta["ok"]:
        r = respuesta["resultado"]
        print(f"Tarea creada: #{r['id']} - {r['titulo']}")
    else:
        print(f"❌ {respuesta['error']}")
 
 
def listar_tareas():
    respuesta = enviar_pedido({"accion": "listar"})
 
    if respuesta["ok"]:
        tareas = respuesta["resultado"]
        if not tareas:
            print("No hay tareas cargadas.")
        else:
            print("\n--- Tareas ---")
            for t in tareas:
                estado = "✔" if t["completa"] else "·"
                print(f"  [{estado}] #{t['id']} {t['titulo']}")
    else:
        print(f"{respuesta['error']}")
 
 
def completar_tarea():
    try:
        id_tarea = int(input("ID de la tarea a completar: ").strip())
    except ValueError:
        print("❌ Tenés que ingresar un número")
        return
 
    respuesta = enviar_pedido({"accion": "completar", "id": id_tarea})
 
    if respuesta["ok"]:
        print(f"{respuesta['resultado']}")
    else:
        print(f"{respuesta['error']}")
 
 
def menu():
    opciones = {
        "1": ("Crear tarea", crear_tarea),
        "2": ("Listar tareas", listar_tareas),
        "3": ("Completar tarea", completar_tarea),
        "4": ("Salir", None),
    }
 
    while True:
        print("\n--- Menú ---")
        for key, (label, _) in opciones.items():
            print(f"  {key}. {label}")
 
        opcion = input("Elegí una opción: ").strip()
 
        if opcion == "4":
            print("Hasta luego")
            break
        elif opcion in opciones:
            _, accion = opciones[opcion]
            try:
                accion()
            except ConnectionRefusedError:
                print("No se pudo conectar al servidor")
        else:
            print("Opción inválida")
 
 
if __name__ == "__main__":
    menu()