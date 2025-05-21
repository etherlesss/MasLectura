# Importar dependencias
from flask import Blueprint, jsonify, request
import datetime

# Crear un objeto Blueprint para la ruta de libros
list_bp = Blueprint('list', __name__)

'''
    RUTAS
'''

# Obtener lista
@list_bp.route('/list/<int:id_lista>', methods=['GET'])
def getList(id_lista):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener la lista de libros
        cur.execute("SELECT * FROM Lista WHERE id_lista = %s", (id_lista,))
        list = cur.fetchone()

        if list is None:
            return jsonify({'message': 'Lista no encontrada'}), 404

        # Respuesta de éxito
        return jsonify(list), 200
    except Exception as err:
        print(f"Error al obtener la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

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

# Obtener libros de una lista
@list_bp.route('/list/<int:id_lista>/books', methods=['GET'])
def getBooks(id_lista):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los libros de la lista
        cur.execute("SELECT * FROM Libro INNER JOIN Libro_Lista ON Libro.id_libro = Libro_Lista.id_libro WHERE Libro_Lista.id_lista = %s", (id_lista,))
        books = cur.fetchall()

        if not books:
            return jsonify({'message': 'No hay libros en la lista'}), 404

        # Respuesta de éxito
        return jsonify(books), 200
    except Exception as err:
        print(f"Error al obtener los libros de la lista: {err}")
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

# Editar lista
@list_bp.route('/list/<int:id_lista>', methods=['PATCH'])
def editList(id_lista):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos de la lista
        data = request.get_json()

        # Enviar no autorizado si la lista es 'Leído', 'Leyendo' o 'Quiero leer'
        if data['nombre_lista'] in ['Leído', 'Leyendo', 'Quiero leer']:
            return 401

        # Actualizar la lista en la base de datos
        cur.execute("UPDATE Lista SET nombre_lista = %s, descripcion = %s WHERE id_lista = %s", (data['nombre_lista'], data['descripcion'], id_lista))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Lista editada exitosamente'}), 200
    except Exception as err:
        print(f"Error al editar la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Eliminar libro de lista
@list_bp.route('/list/<int:id_lista>/book/<int:id_libro>', methods=['DELETE'])
def deleteBookFromList(id_lista, id_libro):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Eliminar el libro de la lista
        cur.execute("DELETE FROM Libro_Lista WHERE id_lista = %s AND id_libro = %s", (id_lista, id_libro))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Libro eliminado de la lista exitosamente'}), 200
    except Exception as err:
        print(f"Error al eliminar el libro de la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Eliminar lista
@list_bp.route('/list/<int:id_lista>', methods=['DELETE'])
def deleteList(id_lista):
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Eliminar la lista
        cur.execute("DELETE FROM Lista WHERE id_lista = %s", (id_lista,))
        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Lista eliminada exitosamente'}), 200
    except Exception as err:
        print(f"Error al eliminar la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Agregar libro a lista
@list_bp.route('/list/add-book', methods=['POST'])
def add_book_to_list():
    from app import mysql
    cur = None
    try:
        data = request.get_json()
        id_lista = data.get('id_lista')
        id_libro = data.get('id_libro')

        if not id_lista or not id_libro:
            return jsonify({'message': 'Faltan datos requeridos'}), 400

        cur = mysql.connection.cursor()
        # Verifica si ya existe la relación para evitar duplicados
        cur.execute("SELECT * FROM libro_lista WHERE id_lista = %s AND id_libro = %s", (id_lista, id_libro))
        existe = cur.fetchone()
        if existe:
            return jsonify({'message': 'El libro ya está en la lista'}), 409

        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(
            "INSERT INTO libro_lista (id_lista, id_libro, fecha) VALUES (%s, %s, %s)",
            (id_lista, id_libro, fecha)
        )
        mysql.connection.commit()
        return jsonify({'message': 'Libro agregado a la lista exitosamente'}), 201
    except Exception as err:
        print(f"Error al agregar libro a la lista: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        if cur: cur.close()