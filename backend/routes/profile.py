# Importar dependencias
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import bcrypt
import os

# Cargar variables de entorno
load_dotenv()

# Definir variables
SALT_ROUNDS = os.getenv("SALT_ROUNDS")

# Crear un objeto Blueprint para la ruta de perfil
profile_bp = Blueprint('profile', __name__)

'''
    RUTAS
'''

# Obtener los datos del usuario por id
@profile_bp.route('/profile/<int:id_usuario>', methods=['GET'])
def getProfile(id_usuario):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos del usuario
        cur.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'message': 'El usuario no existe'}), 404
        
        # Respuesta de éxito
        return user, 200
    except Exception as err:
        print(f"Error al obtener el perfil del usuario: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Obtener las listas del usuario por id
@profile_bp.route('/profile/<int:id_usuario>/lists', methods=['GET'])
def getLists(id_usuario):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener las listas del usuario
        cur.execute("SELECT * FROM Lista WHERE id_usuario = %s", (id_usuario,))
        lists = cur.fetchall()

        if not lists:
            return jsonify({'message': 'El usuario no tiene listas'}), 404

        # Respuesta de éxito
        return jsonify(lists), 200
    except Exception as err:
        print(f"Error al obtener lista(s) del usuario: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Actualizar los datos del usuario
@profile_bp.route('/profile/<int:id_usuario>', methods=['PATCH'])
def updateProfile(id_usuario):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos del usuario
        cur.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'message': 'El usuario no existe'}), 404

        # Actualizar los datos del usuario
        data = request.get_json()
        cur.execute("UPDATE Usuario SET nombre_usuario = %s, mail_usuario = %s, genero_usuario = %s, fecha_nacimiento = %s, foto_perfil = %s WHERE id_usuario = %s", (data['nombre_usuario'], data['mail_usuario'], data['genero_usuario'], data['fecha_nacimiento'], data.get('foto_perfil', None), id_usuario))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Perfil actualizado correctamente'}), 200
    except Exception as err:
        print(f"Error al actualizar el perfil del usuario: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Cambiar la contraseña del usuario
@profile_bp.route('/profile/<int:id_usuario>/change-password', methods=['PATCH'])
def updatePwd(id_usuario):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos del usuario
        cur.execute("SELECT * FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'message': 'El usuario no existe'}), 404

        # Obtener la nueva contraseña
        data = request.get_json()

        # Validar que la contraseña actual es correcta
        if not bcrypt.checkpw(data['pwdCurrent'].encode('utf-8'), user['contrasenia'].encode('utf-8')):
            return jsonify({'message': 'La contraseña actual es incorrecta'}), 401

        # Hash de la nueva contraseña
        pwdHash = bcrypt.hashpw(data['pwd'].encode('utf-8'), bcrypt.gensalt(int(SALT_ROUNDS))).decode('utf-8')

        cur.execute("UPDATE Usuario SET contrasenia = %s WHERE id_usuario = %s", (pwdHash, id_usuario))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Contraseña actualizada correctamente'}), 200
    except Exception as err:
        print(f"Error al actualizar la contraseña del usuario: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()