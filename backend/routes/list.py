# Importar dependencias
from flask import Blueprint, jsonify, request

# Crear un objeto Blueprint para la ruta de libros
list_bp = Blueprint('list', __name__)

'''
    RUTAS
'''

# Obtener el primer libro de una lista por su ID
@list_bp.route('/list/<int:id_lista>/first-book', methods=['GET'])
def getFirstBook(id_lista):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener el primer libro de la lista
        cur.execute("SELECT * FROM Libro INNER JOIN Libro_Lista ON Libro.id_libro = Libro_Lista.id_libro WHERE Libro_Lista.id_lista = %s LIMIT 1", (id_lista,))
        book = cur.fetchone()

        if book is None:
            return jsonify({'message': 'No hay libros en la lista'}), 404

        # Respuesta de éxito
        return jsonify(book), 200
    except Exception as err:
        print(f"Error al obtener el primer libro de la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Crear lista 
@list_bp.route('/list', methods=['POST'])
def createList():
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos de la lista
        data = request.get_json()
        
        # Insertar la lista en la base de datos
        cur.execute("INSERT INTO Lista (id_usuario, nombre_lista, descripcion) VALUES (%s, %s, %s)", (data['id_usuario'], data['nombre_lista'], data['descripcion']))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Lista creada exitosamente'}), 201
    except Exception as err:
        print(f"Error al crear la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()