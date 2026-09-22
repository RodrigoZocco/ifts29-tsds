import threading

def contar(inicio, fin, nombre):
    for i in range(inicio, fin + 1):
        print(f"Hilo {nombre}: {i}")

if __name__ == "__main__":
    # Crear los hilos
    hilo1 = threading.Thread(target=contar, args=(1, 5, "A"))
    hilo2 = threading.Thread(target=contar, args=(6, 10, "B"))

    # Iniciar los hilos
    hilo1.start()
    hilo2.start()

    # Esperar que terminen
    hilo1.join()
    hilo2.join()

    print("Conteo terminado")


'''
Cada hilo imprime su rango de números.

No usamos sleep ni Event, entonces el orden no está garantizado.

Significa que los números del 1 al 10 se van a imprimir mezclados dependiendo del scheduler de Python y del GIL.
'''