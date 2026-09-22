## Clase 3 "Sistema Distribuido, CDN y DDoS"
### Sistema Distribuido
- Conjunto formado por computadoras o nodos que colaboran para 1 objetivo comun. operan de manera independiente pero coordinada. 
- Los nodos funcionan en paralelo, comparten recursos y se coordinan para ejecutar una tarea
- Tipos de sistemas distribuidos:
  - Homogéneos: Nodos todos iguales en cuanto a hardware y software. 
  - Heterogéneos: Nodos con distintas configs, hardware y software. Ej: IoT, donde los nodos son sensores, actuadores y servidores con dif. caracteristicas
  - En tiempo real: Hilos son más ligeros que los procesos pq comparten el mismo espacio de memoria. crear y gestionar hilos es mas eficiente que crear N procesos
### CDN "Content Delivery Network"
- Conjunto de servidores geograficamente distribuidos que agilizan la entrega de contenido web cacheandolo en la ubicación más cercana al usuario.
  - EJ: Mientras mas lejos 1 cliente esta del host (server), más tardará en cargarle. CDN es un conjunto de servers distribuidos que estan entre el cliente y el servidor origen, para cargar más rapido
### DDoS (distributed denial ofservice)
- Saturación de un server o servicio o red "inundandolo" de trafico de internet
  - Usa Muchisimas computadoras comprometidas como fuentes de ataque (PCs e IoT devices hackeados) 
- Funcionamiento: 
  - Devices infectados conectados a internet (controladas en remoto por el hacker)
    - Llamados `bots o zombies`, y el grupo de bots se llama `botnet`
  - Hacker envia instrucciones a cada bot y este envia requests al IP objetivo (saturandola y denegando el servicio al trafico normal)
- Tipos de ataques:
  - Volumetric Attacks
    - Congestiona consumiendo la banda ancha entre el objetivo e internet (envia trafico masivo al target)
  - Protocol Attacks
    - Sobreconsume recursos del server o network firewall/load balancers. layer 3 y 4
  - App Layer attacks
    - Saturar el target con requests
- Mitigacion: Diferenciar entre trafico normal y atacante
  - Rate limiting
  - WAF (Web Application Firewall): Filtrado de trafico basado en una serie de reglas
  - Anycast network diffusion: Uso de Anycast Network, dispersar el trafico atacante en 1 red distribuida
  - Blackhole routing: Crear 1 ruta de agujero negro y canalizar trafico a ella

## Clase 4 "Modelos Cliente Servidor"
- Arquitectura de software con dos roles principales que se comunican
  - `Cliente`: Componente o Dispositivo, solicita servicios o recursos a otro (el servidor)
    - Generan una UI para que el usuario interactue (desktop app, web app, mobile app, etc...)
    - Envia peticiones al servidor y espera las respuestas
  - `Servidor`: Componente o Maquina, proporciona servicios, recursos o datos a los clientes que solicitan

- Tipos de sistemas cliente-servidor
  - De una capa (1 solo servidor): Basico, 1 server que atiende a los clientes (Ej: server web q responde peticiones de navegadores)
  - De Dos capas: El server interactua directo con el server, pero este realiza tareas mas complejas (como DBs), server gestiona y devuelve resultados
  - De tres capas: Presentacion (Cliente) > Logica de negocio (Servidor intermedio) > Capa de datos (Server de DB). Escalabilidad y modularidad
  - Basado en la nube: Servidor distribuido en datacenters a través de internet
- Ejemplos: Correo Electronico (Como SMTP, clientes como Outlook o Gmail se comunican con servers de correo), Servicios Web (Facebook, Twitter), Juegos en linea (cliente se conecta al server central)