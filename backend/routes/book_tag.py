from flask import Blueprint, request, jsonify

book_tag_bp = Blueprint('book_tag', __name__)

@book_tag_bp.route('/book_tag', methods=['POST'])
def addBookTags():
    from app import mysql  # <-- Importa aquí, dentro de la función
    try:
        data = request.get_json()
        id_libro = data.get('id_libro')
        etiquetas = data.get('etiquetas', [])

        if not id_libro or not etiquetas or not isinstance(etiquetas, list):
            return jsonify({'message': 'Faltan datos requeridos'}), 400

        cur = mysql.connection.cursor()
        for id_etiquetas in etiquetas:
            cur.execute(
                "INSERT INTO libro_etiquetas (id_libro, id_etiquetas) VALUES (%s, %s)",
                (id_libro, id_etiquetas)
            )
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Etiquetas asociadas correctamente'}), 201
    except Exception as err:
        print(f"Error al asociar etiquetas: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500