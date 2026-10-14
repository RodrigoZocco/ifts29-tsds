# Rodrigo Zocco - PFO 2

## Instrucciones para ejecutar el proyecto
```
pip install -r requirements.txt
python app.py
python cliente.py
```
- En la terminal que se ejecuta `python cliente.py` se podrá elegir cada opcion y que se llame al API programaticamente
- La carpeta `imagenes-pruebas-exitosas` contiene las capturas de pantalla de pruebas exitosas.

## ¿Por qué hashear contraseñas?
Para evitar que si alguien accede y roba tu base de datos, no consiga las contraseñas reales (no va a poder loguearse) ya que guardar un hash no se puede "revertir" y obtener el string hasheado para obtener el original. Ej: en vez de guardar "contraseña123", se guarda el hash que genera Bcrypt y se ve algo asi "$2b$12$xK9". Al loguearse el usuario deberá introducir su contraseña y se hasheara, si coincide con la guardada es el usuario real.

## Ventajas de usar SQLite en este proyecto
Porque no hay que configurar nada ni levantar ningun servidor, es un archivo .db, ademas viene con python y no hace falta instalar nada extra. Finalmente porque es un proyecto chico para aprender/prototipo. Si el proyecto creciera y necesite soportar más usuarios a la vez (escalar) es cuando se podría migrar, pero como para nuestros requerimientos SQLite cumple, lo usamos sin agregar complejidad. Además en materias de anteriores años ya hemos levantado bases de datos relaciones y no relaciones de la forma real, por lo que si queremos hacer el cambio sabemos como.

## Aclaraciones
- GitHub Pages solo sirve para sitios estáticos y no ejecuta python ni ningun backend, por lo que no se puede deployear ahi.