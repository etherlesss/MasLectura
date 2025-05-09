# Importar dependencias
from flask import Blueprint, jsonify, request

# Crear un objeto Blueprint para la ruta de libros
book_bp = Blueprint('book', __name__)

'''
    RUTAS
'''

# Agregar un libro a la base de datos
@book_bp.route('/book', methods=['POST'])
def addBook():
    from app import mysql
    cur = None
    try:
        # Obtener la conexion a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos del libro
        data = request.get_json()

        tipo = data.get('tipo')
        titulo = data.get('titulo')
        autor = data.get('autor')
        editorial = data.get('editorial')
        fecha_publicacion = data.get('fechaPublicacion')
        idioma = data.get('idioma')
        numero_capiutlos = data.get('numeroCapitulos')
        enlace = data.get('url')
        finalizado = data.get('serieFinalizada')
        portada = data.get('portada')
        sinopsis = data.get('sinopsis')

        # Insertar el libro en la base de datos
        cur.execute(
            """
            INSERT INTO Libro (id_usuario, titulo, autor, fecha_publicacion, portada, promedio, tipo_libro, editorial)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (1, titulo, autor, fecha_publicacion, '', 0, tipo, editorial)
        )

        mysql.connection.commit()

        # Respuesta de éxito
        return jsonify({'message': 'Libro agregado exitosamente'}), 201
    except Exception as err:
        print(f"Error al agregar el libro: {err}")
        return jsonify({'message': 'Error interno del servidor'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()
