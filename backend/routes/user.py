from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/role/<int:id_usuario>', methods=['GET'])
def get_user_role(id_usuario):
    from app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT rol FROM usuario WHERE id_usuario = %s", (id_usuario,))
        row = cur.fetchone()
        cur.close()
        if row:
            return jsonify({'rol': row['rol']}), 200
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except Exception as e:
        print(f"Error en get_user_role: {e}")
        return jsonify({'error': 'Error interno al obtener el rol'}), 500
    

@user_bp.route('/user/<int:id_usuario>', methods=['DELETE', 'OPTIONS'])
def delete_user(id_usuario):
    if request.method == 'OPTIONS':
        return '', 200
    from app import mysql
    try:
        cur = mysql.connection.cursor()
        # Borra calificaciones del usuario
        cur.execute("DELETE FROM calificacion_usuario WHERE id_usuario = %s", (id_usuario,))
        # Borra comentarios del usuario
        cur.execute("DELETE FROM comentario WHERE id_usuario = %s", (id_usuario,))
        # Borra listas del usuario
        cur.execute("DELETE FROM lista WHERE id_usuario = %s", (id_usuario,))
        # Borra libros del usuario (si aplica)
        cur.execute("DELETE FROM libro WHERE id_usuario = %s", (id_usuario,))
        # Finalmente, borra el usuario
        cur.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Usuario eliminado'}), 200
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return jsonify({'error': 'Error interno al eliminar usuario'}), 500
    

@user_bp.route('/user/<int:id_usuario>/nombre', methods=['PATCH'])
def update_user_name(id_usuario):
    from app import mysql
    data = request.get_json()
    nuevo_nombre = data.get('nombre_usuario')
    if not nuevo_nombre:
        return jsonify({'message': 'Falta el nombre de usuario'}), 400
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuario SET nombre_usuario = %s WHERE id_usuario = %s", (nuevo_nombre, id_usuario))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Nombre de usuario actualizado'}), 200
    except Exception as e:
        print(f"Error al actualizar nombre de usuario: {e}")
        return jsonify({'error': 'Error interno al actualizar nombre de usuario'}), 500