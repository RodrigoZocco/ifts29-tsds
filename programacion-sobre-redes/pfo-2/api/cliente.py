import requests

BASE_URL = "http://127.0.0.1:5000"

# Esto lo hice para mantener la session entre requests
session = requests.Session()


def registrar():
    usuario   = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    r = session.post(f"{BASE_URL}/registro", json={"usuario": usuario, "contraseña": contrasena})
    data = r.json()

    if r.status_code == 201:
        print(f"✅ {data['mensaje']}")
    else:
        print(f"❌ {data['error']}")


def login():
    usuario   = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    r = session.post(f"{BASE_URL}/login", json={"usuario": usuario, "contraseña": contrasena})
    data = r.json()

    if r.status_code == 200:
        print(f"✅ {data['mensaje']}")
    else:
        print(f"❌ {data['error']}")


def ver_tareas():
    r = session.get(f"{BASE_URL}/tareas")

    if r.status_code == 200:
        print("Acceso concedido. El servidor devolvió la página de tareas.")
    else:
        print(f"❌ {r.json()['error']}")


def menu():
    opciones = {
        "1": ("Registrarse",  registrar),
        "2": ("Iniciar sesión", login),
        "3": ("Ver tareas",   ver_tareas),
        "4": ("Salir",        None),
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
            accion()
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
