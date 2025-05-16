from flask import Blueprint, jsonify

genre_bp = Blueprint('genre', __name__)

@genre_bp.route('/genre', methods=['GET'])
def get_generos():
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_genero as id, nombre_genero AS nombre, descripcion AS descripcion FROM Genero ORDER BY nombre_genero ASC")
        generos = cur.fetchall()
        
        # Agregar impresión para depurar la respuesta
        print("Géneros obtenidos:", generos)
        
        return jsonify(generos), 200
    except Exception as err:
        print(f"Error al obtener géneros: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        if cur: cur.close()
