# Importar dependencias
from flask import Blueprint, request, jsonify
from flask_mail import Message
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import bcrypt
import secrets

# Cargar variables de entorno
load_dotenv()

# Definir variables
SALT_ROUNDS = os.getenv("SALT_ROUNDS")

# Crear un objeto Blueprint para la ruta de recuperación de contraseña
recover_password_bp = Blueprint('recover-password', __name__)

@recover_password_bp.route('/recover-password', methods=['PATCH'])
def recoverPwd():
    from app import mysql, mail
    cur = None
    try:
        data = request.get_json()
        email = data.get('mail')

        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Verificar si el correo electrónico existe en la base de datos
        cur.execute("SELECT * FROM Usuario WHERE mail_usuario = %s", (email,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'message': 'El correo electrónico no está registrado'}), 404
        
        # Generar un token único para la recuperación de contraseña
        token = secrets.token_hex(16)
        exp_time =  datetime.now() + timedelta(hours=1)

        # Guardar el token y la fecha de expiración en la base de datos
        cur.execute("UPDATE Usuario SET token_recuperacion = %s, exp_recuperacion = %s WHERE mail_usuario = %s", (token, exp_time, email))
        mysql.connection.commit()

        # Crear enlace de recuperación
        recovery_link = f"http://localhost:5173/recover-password/token={token}"

        # Configurar el correo electrónico
        msg = Message(
            subject="+Lectura | Recuperar contraseña",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[email],
            body=f"Hola, \n\nPara recuperar tu contraseña, haz clic en el siguiente enlace: {recovery_link}\n\nSi no solicitaste esta recuperación, ignora este correo.\n\nGracias,\nEquipo +Lectura"
        )
        mail.send(msg)

        return jsonify({'message': 'Correo de recuperación enviado'}), 200
    except Exception as err:
        print(f"Error al enviar el correo de recuperación: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

@recover_password_bp.route('/reset-password', methods=['PATCH'])
def resetPwd():
    from app import mysql
    cur = None
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('pwd')

        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Verificar si el token es válido y no ha expirado
        cur.execute("SELECT * FROM Usuario WHERE token_recuperacion = %s AND exp_recuperacion > NOW()", (token,))
        user = cur.fetchone()

        if user is None:
            return jsonify({'message': 'Token inválido o expirado'}), 404
        
        # Actualizar la contraseña del usuario
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(int(SALT_ROUNDS)))
        cur.execute("UPDATE Usuario SET contrasenia = %s, token_recuperacion = NULL, exp_recuperacion = NULL WHERE mail_usuario = %s", (hashed_password, user['mail_usuario']))
        mysql.connection.commit()

        return jsonify({'message': 'Contraseña actualizada con éxito'}), 200
    except Exception as err:
        print(f"Error al restablecer la contraseña: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

@recover_password_bp.route('/test-email', methods=['GET'])
def test_email():
    from app import mail
    try:
        msg = Message(
            subject="Correo de prueba",
            sender=os.getenv('MAIL_USERNAME'),
            recipients=["quinngtr800@gmail.com"],  # Cambia esto por un correo válido
            body="Este es un correo de prueba enviado desde Flask."
        )
        mail.send(msg)
        return jsonify({'message': 'Correo enviado exitosamente'}), 200
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return jsonify({'message': 'Error al enviar el correo'}), 500