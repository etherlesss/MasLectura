from flask import Blueprint, jsonify

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tag', methods=['GET'])
def get_etiquetas():
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  id_etiqueta as id, nombre_etiqueta AS nombre, descripcion as descripcion FROM Etiqueta")
        etiquetas = cur.fetchall()
        return jsonify(etiquetas), 200
    except Exception as err:
        print(f"Error al obtener etiquetas: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        if cur: cur.close()