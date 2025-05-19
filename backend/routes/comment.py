from flask import Blueprint, request, jsonify

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comentario', methods=['POST'])
def add_comment():
    from app import mysql
    data = request.get_json()
    id_libro = data.get('id_libro')
    id_usuario = data.get('id_usuario') 
    descripcion = data.get('descripcion')

    if not id_libro or not id_usuario or not descripcion:
        return jsonify({'message': 'Faltan datos requeridos'}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO comentario (id_usuario, descripcion, id_libro) VALUES (%s, %s, %s)",
        (id_usuario, descripcion, id_libro)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Comentario guardado correctamente'}), 201


@comment_bp.route('/comentario/<int:id_libro>', methods=['GET'])
def get_comments(id_libro):
    try:
        from app import mysql
        cur = mysql.connection.cursor()
        cur.execute(
        """
        SELECT u.nombre_usuario, c.descripcion
        FROM comentario c
        JOIN usuario u ON c.id_usuario = u.id_usuario
        WHERE c.id_libro = %s
        ORDER BY c.id_comentario DESC
        """,
        (id_libro,)
    )
        rows = cur.fetchall()
        comentarios = [
            {"nombre_usuario": row["nombre_usuario"], "descripcion": row["descripcion"]}
            for row in rows
        ]
        cur.close()
        return jsonify(comentarios), 200
    except Exception as e:
        print(f"Error en get_comments: {e}")
        return jsonify({"error": "Error interno al obtener comentarios"}), 500
