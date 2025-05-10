# Importar dependencias
from flask import Blueprint, jsonify, request

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
        cur.execute("UPDATE Usuario SET nombre_usuario = %s, mail_usuario = %s, genero_usuario = %s, fecha_nacimiento = %s WHERE id_usuario = %s", (data['nombre_usuario'], data['mail_usuario'], data['genero_usuario'], data['fecha_nacimiento'], id_usuario))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Perfil actualizado correctamente'}), 200
    except Exception as err:
        print(f"Error al actualizar el perfil del usuario: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()