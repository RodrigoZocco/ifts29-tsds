from flask import Flask, request, jsonify, render_template_string, session
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "en-produccion-viene-de-env-vars")

DB_PATH = "base_de_datos.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario   TEXT    NOT NULL UNIQUE,
                password  TEXT    NOT NULL
            )
        """)
        conn.commit()

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "Se esperaba JSON"}), 400

    usuario   = datos.get("usuario", "").strip()
    contrasena = datos.get("contraseña", "")

    if not usuario or not contrasena:
        return jsonify({"error": "usuario y contraseña son obligatorios"}), 400

    if len(contrasena) < 4:
        return jsonify({"error": "La contraseña debe tener al menos 4 caracteres"}), 400

    hash_pw = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (?, ?)",
                (usuario, hash_pw.decode())
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": f"Usuario '{usuario}' registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "Se esperaba JSON"}), 400

    usuario   = datos.get("usuario", "").strip()
    contrasena = datos.get("contraseña", "")

    if not usuario or not contrasena:
        return jsonify({"error": "usuario y contraseña son obligatorios"}), 400

    with get_db() as conn:
        fila = conn.execute(
            "SELECT password FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()

    if fila is None or not bcrypt.checkpw(contrasena.encode(), fila["password"].encode()):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    session["usuario"] = usuario
    return jsonify({"mensaje": f"Bienvenido, {usuario}"}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    if "usuario" not in session:
        return jsonify({"error": "No autorizado Inicia sesion primero en /login"}), 401

    html = render_template_string(TEMPLATE_TAREAS, usuario=session["usuario"])
    return html, 200


# ---------------------------------------------------------------------------
# Template HTML
# ---------------------------------------------------------------------------

TEMPLATE_TAREAS = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Tareas</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 60px auto; padding: 0 20px; }
        h1   { color: #333; }
        p    { color: #555; }
    </style>
</head>
<body>
    <h1>👋 Hola, {{ usuario }}!</h1>
    <p>Iniciaste sesión correctamente. Acá irían tus tareas.</p>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Arranque
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
