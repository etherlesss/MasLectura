# Importar dependencias
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import bcrypt
import jwt
import os
import time

# Cargar variables de entorno
load_dotenv()

# Crear un objeto Blueprint para la ruta de inicio de sesión
login_bp = Blueprint('login', __name__)

# Clave secreta para firmar el token JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

'''
    RUTAS
'''

# Inicio de sesión
@login_bp.route('/login', methods=['POST'])
def login():
    from app import mysql
    cur = None
    try:
        data = request.get_json()
        mail = data.get('mail')
        pwd = data.get('pwd')

        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Consultar el usuario en la base de datos
        cur.execute("SELECT * FROM Usuario WHERE mail_usuario = %s", (mail,))
        user = cur.fetchone()

        # Comprobar si el usuario existe
        if user is None:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        
        # Comprobar la contraseña
        if not bcrypt.checkpw(pwd.encode('utf-8'), user['contrasenia'].encode('utf-8')):
            return jsonify({'message': 'Contraseña incorrecta'}), 401
        
        # Generar el token JWT con expiracion de 4 horas
        token = jwt.encode({
            'id': user['id_usuario'],
            'mail': user['mail_usuario'],
            'exp': int(time.time() + (4 * 60 * 60)),  # 4 horas
        }, JWT_SECRET_KEY, algorithm='HS256')

        # Asegurarse de que el token sea una cadena
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        # Obtener la fecha de expiracion del token
        exp_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + (4 * 60 * 60)))

        # Enviar la respuesta con el token y la fecha de expiracion
        return jsonify({
            'user': {
                'id': user['id_usuario'],
                'name': user['nombre_usuario'],
                'mail': user['mail_usuario']
            },
            'token': token,
            'exp_date': exp_date
        }), 200
    except Exception as err:
        print(f"Error al iniciar sesion: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()