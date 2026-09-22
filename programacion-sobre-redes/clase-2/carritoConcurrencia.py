import threading
import time

stock = 10
lock = threading.Lock()

def comprar(nombre, cantidad):
    global stock
    print(f"{nombre} intenta comprar {cantidad} unidades...")
    with lock:  # proteger la sección crítica
        if stock >= cantidad:
            time.sleep(0.1)
            stock -= cantidad
            print(f"{nombre} compró {cantidad} unidades. Stock restante: {stock}")
        else:
            print(f"{nombre} no pudo comprar, stock insuficiente ({stock})")

cliente1 = threading.Thread(target=comprar, args=("Cliente 1", 7))
cliente2 = threading.Thread(target=comprar, args=("Cliente 2", 7))

cliente1.start()
cliente2.start()
cliente1.join()
cliente2.join()

print(f"Stock final: {stock}")
