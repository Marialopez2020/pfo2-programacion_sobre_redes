from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "database.db"

def init_db():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

init_db()

@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    hash_contrasena = generate_password_hash(contrasena)

    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hash_contrasena))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 400

@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña") or datos.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado and check_password_hash(resultado[0], contrasena):
        return jsonify({"mensaje": "Inicio de sesion exitoso", "acceso": True}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route("/tareas", methods=["GET"])
def tareas():
    return render_template("bienvenida.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
