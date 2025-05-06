# Importar dependencias
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import bcrypt
import os

# Cargar variables de entorno
load_dotenv()

# Definir variables
SALT_ROUNDS = os.getenv("SALT_ROUNDS")

# Crear un objeto Blueprint para la ruta de registro
signup_bp = Blueprint('signup', __name__)

'''
    RUTAS
'''

# Registro de usuario
@signup_bp.route('/signup', methods=['POST'])
def signup():
    from app import mysql
    cur = None
    try:
        data = request.get_json()
        username = data.get('username')
        mail = data.get('mail')
        pwd = data.get('pwd')
        bdate = data.get('birthdate')
        gender = data.get('gender')

        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Comprobar si el usuario ya existe
        cur.execute("SELECT * FROM Usuario WHERE mail_usuario = %s", (mail,))
        user = cur.fetchone()
        if user is not None:
            return jsonify({'message': 'El usuario ya existe'}), 409
        
        # Hashear la contraseña
        pwdHash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt(int(SALT_ROUNDS))).decode('utf-8')

        # Insertar el nuevo usuario en la base de datos
        cur.execute("INSERT INTO Usuario (nombre_usuario, mail_usuario, contrasenia, genero_usuario, rol, fecha_nacimiento) VALUES (%s, %s, %s, %s, 'Usuario', %s)", (username, mail, pwdHash, gender, bdate,))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as err:
        print(f"Error al registrar el usuario: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()
