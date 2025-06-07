from flask import Blueprint, request, jsonify
from datetime import date

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comentario', methods=['POST'])
def add_comment():
    from app import mysql
    data = request.get_json()
    id_libro = data.get('id_libro')
    id_usuario = data.get('id_usuario') 
    descripcion = data.get('descripcion')
    fecha = data.get('fecha')

    if not id_libro or not id_usuario or not descripcion:
        return jsonify({'message': 'Faltan datos requeridos'}), 400
    
    if not fecha:
        fecha = date.today()

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO comentario (id_usuario, descripcion, id_libro, fecha) VALUES (%s, %s, %s, %s)",
        (id_usuario, descripcion, id_libro, fecha)
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
        SELECT c.id_usuario, c.id_comentario, u.nombre_usuario, u.foto_perfil, c.descripcion, c.fecha
        FROM comentario c
        JOIN usuario u ON c.id_usuario = u.id_usuario
        WHERE c.id_libro = %s
        ORDER BY c.id_comentario DESC
        """,
        (id_libro,)
    )
        rows = cur.fetchall()
        comentarios = [
            { "id_usuario": row["id_usuario"],"id_comentario": row["id_comentario"], "nombre_usuario": row["nombre_usuario"],  "foto_perfil": row["foto_perfil"], "descripcion": row["descripcion"], "fecha": row["fecha"].isoformat() if row["fecha"] else None}
            for row in rows
        ]
        cur.close()
        return jsonify(comentarios), 200
    except Exception as e:
        print(f"Error en get_comments: {e}")
        return jsonify({"error": "Error interno al obtener comentarios"}), 500
    

@comment_bp.route('/comentario/<int:id_comentario>', methods=['DELETE'])
def delete_comment(id_comentario):
    try:
        from app import mysql
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM comentario WHERE id_comentario = %s", (id_comentario,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Comentario eliminado correctamente'}), 200
    except Exception as e:
        print(f"Error al eliminar comentario: {e}")
        return jsonify({'error': 'Error interno al eliminar comentario'}), 500
