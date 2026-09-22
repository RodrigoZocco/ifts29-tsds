import threading

def contar(inicio, fin, mi_turno, turno_otro, nombre):
    for i in range(inicio, fin + 1):
        mi_turno.wait()        # Espera a que sea su turno
        mi_turno.clear()       # Consume el turno
        print(f"Hilo {nombre}: {i}")
        turno_otro.set()       # Da paso al otro hilo

if __name__ == "__main__":
    # Eventos para controlar turnos
    turno_A = threading.Event()
    turno_B = threading.Event()

    # Crear los hilos
    hilo1 = threading.Thread(target=contar, args=(1, 5, turno_A, turno_B, "A"))
    hilo2 = threading.Thread(target=contar, args=(6, 10, turno_B, turno_A, "B"))

    # Iniciar los hilos
    hilo1.start()
    hilo2.start()

    # Comienza el turno del hilo A
    turno_A.set()

    # Esperar que ambos terminen
    hilo1.join()
    hilo2.join()

    print("Conteo terminado")
    
'''
CONCURRENCIA CON EVENT
Usamos threading.Event() como semáforo binario.

Solo el hilo cuyo Event esté activo (.set()) puede imprimir.

Al terminar su número, ese hilo cede el turno al otro.
'''

    
