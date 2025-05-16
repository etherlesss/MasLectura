from flask import Blueprint, request, jsonify

book_genre_bp = Blueprint('book_genre', __name__)

@book_genre_bp.route('/book_genre', methods=['POST'])
def addBookGenres():
    from app import mysql  # Importa aquí para evitar importación circular
    try:
        data = request.get_json()
        id_libro = data.get('id_libro')
        generos = data.get('generos', [])

        if not id_libro or not generos or not isinstance(generos, list):
            return jsonify({'message': 'Faltan datos requeridos'}), 400

        cur = mysql.connection.cursor()
        for id_genero in generos:
            cur.execute(
                "INSERT INTO libro_genero (id_genero, id_libro) VALUES (%s, %s)",
                (id_genero, id_libro)
            )
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Géneros asociados correctamente'}), 201
    except Exception as err:
        print(f"Error al asociar géneros: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500