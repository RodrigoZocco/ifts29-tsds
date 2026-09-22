# Crea un programa que simule dos hilos sumando números. Ambos hilos deben sumar números del 1 al 5, 
# pero no deben imprimir el resultado de la suma hasta que  ambos hayan completado la suma de los 5 
# números. Utiliza una variable de condición para asegurar que los resultados 
# solo se impriman una vez que ambos hilos hayan terminado su tarea.

import threading
 
# Variable de condición para sincronización
condicion = threading.Condition()
 
# Variables globales
resultados = []
 
def sumar_numeros(nombre):
    total = 0
    for i in range(1, 6):
        total += i
    with condicion:
        resultados.append(f"{nombre} sumó: {total}")
        condicion.notify_all()  # Notificar que se ha terminado la suma
 
def imprimir_resultados():
    with condicion:
        while len(resultados) < 2:
            condicion.wait()  # Esperar hasta que ambos hilos hayan terminado
        for resultado in resultados:
            print(resultado)
 
hilo1 = threading.Thread(target=sumar_numeros, args=("Hilo 1",))
hilo2 = threading.Thread(target=sumar_numeros, args=("Hilo 2",))
 
hilo1.start()
hilo2.start()
 
# Imprimir los resultados una vez que ambos hilos hayan terminado
imprimir_resultados()