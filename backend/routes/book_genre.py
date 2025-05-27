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
    
@book_genre_bp.route('/book_genre/<int:id_libro>', methods=['GET'])
def get_book_generos(id_libro):
    from app import mysql
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nombre_genero
        FROM genero
        JOIN libro_genero ON libro_genero.id_genero = genero.id_genero
        WHERE libro_genero.id_libro = %s
    """, (id_libro,))
    generos = [row['nombre_genero'] for row in cur.fetchall()]
    cur.close()
    return jsonify(generos), 200


#Actualizar géneros de un libro
@book_genre_bp.route('/book_genre/edit/<int:id_libro>', methods=['PUT'])
def update_book_generos(id_libro):
    from app import mysql
    try:
        data = request.get_json()
        generos = data.get('generos', [])
        if not isinstance(generos, list):
            return jsonify({'message': 'El campo "generos" debe ser una lista'}), 400

        cur = mysql.connection.cursor()
        # Eliminar géneros actuales
        cur.execute("DELETE FROM libro_genero WHERE id_libro = %s", (id_libro,))
        # Insertar los nuevos géneros (por nombre)
        for nombre_genero in generos:
            cur.execute("SELECT id_genero FROM genero WHERE nombre_genero = %s", (nombre_genero,))
            row = cur.fetchone()
            if row:
                id_genero = row['id_genero']
                cur.execute(
                    "INSERT INTO libro_genero (id_genero, id_libro) VALUES (%s, %s)",
                    (id_genero, id_libro)
                )
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Géneros actualizados correctamente'}), 200
    except Exception as err:
        print(f"Error al actualizar géneros: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500