import threading
import time
import random

contador = 0  # recurso compartido

def incrementar():
    global contador
    for _ in range(100000):
        tmp = contador
        # forzar cambio de contexto artificial
        time.sleep(random.uniform(0, 0.00001))
        contador = tmp + 1

# Crear dos hilos
hilo1 = threading.Thread(target=incrementar)
hilo2 = threading.Thread(target=incrementar)

hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

print("Resultado final (sin lock):", contador)

