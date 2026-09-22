import threading
import time
import random

class Servidor:
    def __init__(self, nombre, cluster):
        self.nombre = nombre
        self.archivos = {}  # {archivo: contenido}
        self.cluster = cluster
        self.vivo = True
        self.lock = threading.Lock()

    def subir(self, archivo, contenido):
        if not self.vivo:
            print(f"[{self.nombre}] ❌ No disponible para subir {archivo}")
            return
        with self.lock:
            self.archivos[archivo] = contenido
        print(f"[{self.nombre}] 📤 Subido {archivo}")
        # replicar
        self.cluster.replicar(self, archivo, contenido)

    def descargar(self, archivo):
        if not self.vivo:
            print(f"[{self.nombre}] ❌ No disponible para descargar {archivo}")
            return None
        with self.lock:
            return self.archivos.get(archivo, None)

    def sincronizar(self, archivo, contenido):
        if self.vivo:
            with self.lock:
                self.archivos[archivo] = contenido
            print(f"[{self.nombre}] 🔄 Replica recibida: {archivo}")

    def caer(self):
        self.vivo = False
        print(f"⚠️ {self.nombre} cayó!")

    def levantar(self):
        self.vivo = True
        print(f"✅ {self.nombre} volvió en línea!")


class Cluster:
    def __init__(self):
        self.servidores = []

    def agregar_servidor(self, servidor):
        self.servidores.append(servidor)

    def replicar(self, origen, archivo, contenido):
        for s in self.servidores:
            if s != origen:
                s.sincronizar(archivo, contenido)

    def buscar_servidor(self):
        vivos = [s for s in self.servidores if s.vivo]
        return random.choice(vivos) if vivos else None


# ==== DEMOSTRACIÓN CONCURRENTE ====
cluster = Cluster()
s1 = Servidor("Servidor A", cluster)
s2 = Servidor("Servidor B", cluster)
s3 = Servidor("Servidor C", cluster)
cluster.agregar_servidor(s1)
cluster.agregar_servidor(s2)
cluster.agregar_servidor(s3)

def usuario(nombre):
    for i in range(3):  # cada usuario hace 3 operaciones
        srv = cluster.buscar_servidor()
        if not srv:
            print(f"{nombre} no encontró servidores disponibles")
            return
        archivo = f"{nombre}_file{i}.txt"
        contenido = f"Contenido de {archivo}"
        srv.subir(archivo, contenido)
        time.sleep(random.uniform(0.2, 0.5))
        srv2 = cluster.buscar_servidor()
        if srv2:
            data = srv2.descargar(archivo)
            print(f"{nombre} descargó {archivo} desde {srv2.nombre}: {data}")
        time.sleep(random.uniform(0.2, 0.5))

# Crear 5 usuarios concurrentes
usuarios = [threading.Thread(target=usuario, args=(f"Usuario{i}",)) for i in range(1, 6)]

for u in usuarios:
    u.start()

# Simular caída de un servidor en medio de la actividad
time.sleep(1)
s2.caer()

for u in usuarios:
    u.join()

print("\n Estado final de los servidores:")
for s in cluster.servidores:
    print(f"{s.nombre} ({'vivo' if s.vivo else 'caído'}) → {list(s.archivos.keys())}")
