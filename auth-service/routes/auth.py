from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
from db import get_db_connection
from config import SECRET_KEY
import mysql

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    id = data.get("id")
    tipoId = data.get("tipoId")
    nombre = data.get("nombre")
    contrasena = data.get("contrasena")
    direccion = data.get("direccion")
    correo = data.get("correo")
    telefono = data.get("telefono")
    
    if not id or not tipoId or not nombre or not contrasena or not correo:
        return jsonify({"message": "Faltan datos"}), 400

    hashed_password = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO usuario (id, tipoId, nombre, contrasena, direccion, correo, telefono) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id, tipoId, nombre, hashed_password, direccion, correo, telefono))
        conn.commit()
        return jsonify({"message": "Usuario registrado con éxito"}), 201
    except mysql.connector.Error as err:
        return jsonify({"message": "Error en la base de datos", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    
    if not correo or not contrasena:
        return jsonify({"message": "Faltan datos"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, tipoId, contrasena FROM usuario WHERE correo = %s", (correo,))
        user = cursor.fetchone()

        # Asegurar que se leyó el resultado antes de continuar
        cursor.fetchall()  # Limpia cualquier resultado no leído
        
        if not user:
            return jsonify({"message": "Credenciales incorrectas"}), 401
        
        # bcrypt almacena las contraseñas en bytes, por lo que debemos convertir antes de verificar
        stored_password = user["contrasena"]
        if isinstance(stored_password, bytes):  # Asegurar que es bytes antes de comparar
            stored_password = stored_password.decode("utf-8")

        if not bcrypt.checkpw(contrasena.encode("utf-8"), stored_password.encode("utf-8")):
            return jsonify({"message": "Credenciales incorrectas"}), 401
        
        token = jwt.encode(
            {"id": user["id"], "tipoId": user["tipoId"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})

    except mysql.connector.Error as err:
        return jsonify({"message": "Error en la base de datos", "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()
