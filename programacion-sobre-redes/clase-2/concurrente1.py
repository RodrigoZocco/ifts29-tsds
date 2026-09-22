import threading
import time

def contar(inicio, fin, nombre):
    for i in range(inicio, fin + 1):
        print(f"Hilo {nombre}: {i}")
        # Simular un pequeño retardo para intercalado
        time.sleep(0.3)

if __name__ == "__main__":
    # Crear los hilos
    hilo1 = threading.Thread(target=contar, args=(1, 5, "A"))
    hilo2 = threading.Thread(target=contar, args=(6, 10, "B"))

    # Iniciar los hilos
    hilo1.start()
    hilo2.start()

    # Esperar a que ambos terminen
    hilo1.join()
    hilo2.join()

    print("Conteo terminado")


'''
CONCURRENCIA FORZADA (SLEEP)

hilo1 cuenta de 1 a 5.

hilo2 cuenta de 6 a 10.

Ambos inician con .start() y se ejecutan en paralelo.

time.sleep(0.3) =  hace que los prints se alternen entre hilos (concurrencia visible y forzada con sleep).

.join() =  asegura que el programa principal espere a que ambos hilos terminen antes de imprimir "Conteo terminado".

La salida será concurrente e intercalada, aunque el orden exacto variará en cada ejecución (porque depende del planificador de hilos del sistema operativo).
'''