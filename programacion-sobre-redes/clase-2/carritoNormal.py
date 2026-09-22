import threading
import time

stock = 10  # unidades disponibles

def comprar(nombre, cantidad):
    global stock
    print(f"{nombre} intenta comprar {cantidad} unidades...")
    if stock >= cantidad:
        # Simular tiempo de procesamiento
        time.sleep(0.1)
        stock -= cantidad
        print(f"{nombre} compró {cantidad} unidades. Stock restante: {stock}")
    else:
        print(f"{nombre} no pudo comprar, stock insuficiente ({stock})")

# Dos clientes intentando comprar al mismo tiempo
cliente1 = threading.Thread(target=comprar, args=("Cliente 1", 7))
cliente2 = threading.Thread(target=comprar, args=("Cliente 2", 7))

cliente1.start()
cliente2.start()
cliente1.join()
cliente2.join()

print(f"Stock final: {stock}")
