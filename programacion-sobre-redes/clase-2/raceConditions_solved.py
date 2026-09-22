import threading

contador = 0
lock = threading.Lock()

def incrementar():
    global contador
    for _ in range(100000):
        with lock:  # sección crítica
            contador += 1

hilo1 = threading.Thread(target=incrementar)
hilo2 = threading.Thread(target=incrementar)

hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

print("Resultado final con lock:", contador)


'''
En Python sí hay condiciones de carrera incluso con el GIL.

El GIL no evita problemas de sincronización lógica.

Para evitarlas: Lock, RLock, Semaphore, Queue o usar multiprocessing cuando se trata de CPU-bound.




'''
