# Importar dependencias
from flask import Blueprint, jsonify

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