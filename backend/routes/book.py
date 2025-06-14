# Importar dependencias
from flask import Blueprint, jsonify, request
from datetime import datetime

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
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos del libro
        data = request.get_json()

        # Datos del libro
        id_usuario = data.get('id_usuario', 1)  # Por defecto, asignamos un usuario con ID 1
        titulo = data.get('titulo')
        autor = data.get('autor')
        artista = data.get('artista')
        anio_publicacion = data.get('anio_publicacion')
        portada = data.get('portada', '')
        estado = data.get('estado')
        link_compra = data.get('link_compra')
        promedio = data.get('promedio', 0)
        tipo = data.get('tipo')
        editorial = data.get('editorial')
        idioma = data.get('idioma')
        es_saga = data.get('es_saga')
        titulo_saga = data.get('titulo_saga')
        num_libro = data.get('num_libro')
        num_capitulos = data.get('num_capitulos')
        sinopsis = data.get('sinopsis')



        # Validar datos requeridos
        if not titulo or not autor or not tipo or not estado or not anio_publicacion or not es_saga or not portada:
            # Si falta alguno de los datos requeridos, devolver un error
            return jsonify({'message': 'Faltan datos requeridos'}), 400
        
         # Verificar si el libro ya existe por título y autor
        cur.execute(
            "SELECT id_libro FROM libro WHERE titulo = %s AND autor = %s",
            (titulo, autor)
        )
        libro_existente = cur.fetchone()
        if libro_existente:
            return jsonify({'message': 'El libro ya esta registrado en el base de datos'}), 409

        # Insertar el libro en la base de datos
        cur.execute(
            """
            INSERT INTO libro (
                id_usuario, titulo, autor, artista, anio_publicacion, portada, estado, link_compra,
                promedio, tipo, editorial, idioma, es_saga, titulo_saga, num_libro, num_capitulos, sinopsis
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_usuario, titulo, autor, artista, anio_publicacion, portada, estado, link_compra,
                promedio, tipo, editorial, idioma, es_saga, titulo_saga, num_libro, num_capitulos, sinopsis
            )
        )

        # Obtener el ID del libro recién insertado
        mysql.connection.commit()
        id_libro = cur.lastrowid    

        # Respuesta de éxito
        return jsonify({'message': 'Libro guardado correctamente', 'id_libro': id_libro}), 201
    except Exception as err:
        print(f"Error al agregar el libro: {err}")  # Muestra el error exacto en los logs
        return jsonify({'message': f'Error interno del servidor: {str(err)}'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Obtener todos los libros de la base de datos
@book_bp.route('/books', methods=['GET'])
def getBooks():
    from app import mysql
    cur = None
    try:
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Consultar todos los libros en la base de datos
        cur.execute("SELECT * FROM libro")
        libros = cur.fetchall()

        # Verificar si se encontraron libros
        if not libros:
            return jsonify({'message': 'No se encontraron libros'}), 404
        
        # Respuesta de éxito
        return jsonify(libros), 200
    except Exception as err:
        print(f"Error al obtener los libros: {err}")
        return jsonify({'message': f'Error interno del servidor: {err}'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Obtener todos los libros junto con generos y etiquetas
@book_bp.route('/books/detailed', methods=['GET'])
def getDetailedBooks():
    from app import mysql
    cur = None
    try:
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Consultar todos los libros junto con sus géneros y etiquetas
        cur.execute("""
            SELECT l.id_libro, l.titulo, lg.id_genero, g.nombre_genero, le.id_etiquetas, e.nombre_etiqueta FROM Libro l
            INNER JOIN Libro_Genero lg ON (l.id_libro = lg.id_libro) INNER JOIN Genero g ON (g.id_genero = lg.id_genero)
            INNER JOIN Libro_Etiquetas le ON (l.id_libro = le.id_libro) INNER JOIN Etiqueta e ON (e.id_etiqueta = le.id_etiquetas)
        """)
        libros = cur.fetchall()

        # Verificar si se encontraron libros
        if not libros:
            return jsonify({'message': 'No se encontraron libros'}), 404
        
        # Procesar los resultados para agrupar géneros y etiquetas por libro
        libros_dict = {}
        for libro in libros:
            id_libro = libro['id_libro']
            titulo = libro['titulo']
            id_genero = libro['id_genero']
            nombre_genero = libro['nombre_genero']
            id_etiqueta = libro['id_etiquetas']
            nombre_etiqueta = libro['nombre_etiqueta']

            if id_libro not in libros_dict:
                libros_dict[id_libro] = {
                    'id_libro': id_libro,
                    'titulo': titulo,
                    'generos': [],
                    'etiquetas': []
                }

            # Agregar género
            if id_genero and nombre_genero:
                libros_dict[id_libro]['generos'].append({
                    'id_genero': id_genero,
                    'nombre_genero': nombre_genero
                })

            # Agregar etiqueta
            if id_etiqueta and nombre_etiqueta:
                libros_dict[id_libro]['etiquetas'].append({
                    'id_etiqueta': id_etiqueta,
                    'nombre_etiqueta': nombre_etiqueta
                })

        # Respuesta de éxito
        return jsonify(list(libros_dict.values())), 200
    except Exception as err:
        print(f"Error al obtener los libros detallados: {str(err)}")
        return jsonify({'message': f'Error interno del servidor: {err}'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Obtener un libro por su ID
@book_bp.route('/book/<int:id_libro>', methods=['GET'])
def getBook(id_libro):
    from app import mysql
    cur = None
    try:
        print(f"Buscando libro con id_libro={id_libro}")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM libro WHERE id_libro = %s", (id_libro,))
        libro = cur.fetchone()
        print("Resultado de fetchone():", libro)
        if not libro:
            print("Libro no encontrado en la base de datos.")
            return jsonify({'message': 'Libro no encontrado'}), 404

        return jsonify(libro), 200
    except Exception as err:
        print(f"Error al obtener el libro: {err}")
        return jsonify({'message': f'Error interno del servidor: {str(err)}'}), 500
    finally:
        if cur: cur.close()

# Obtener libros similares por género
@book_bp.route('/books/<int:id_libro>/similar', methods=['GET'])
def getSimilarBooks(id_libro):
    from app import mysql
    cur = None
    try: 
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Consultar generos del libro
        cur.execute("""
            SELECT g.id_genero FROM libro l
            INNER JOIN Libro_Genero lg ON l.id_libro = lg.id_libro
            INNER JOIN Genero g ON lg.id_genero = g.id_genero
            WHERE l.id_libro = %s
        """, (id_libro,))
        generos = cur.fetchall()

        # Verificar si se encontraron géneros
        if not generos:
            return jsonify({'message': 'No se encontraron géneros para el libro'}), 404
        
        # Obtener los IDs de los géneros
        ids_generos = [genero['id_genero'] for genero in generos]

        # Consultar libros similares por género
        cur.execute("""
            SELECT * FROM libro l
            INNER JOIN Libro_Genero lg ON l.id_libro = lg.id_libro
            WHERE lg.id_genero IN %s AND l.id_libro != %s
        """, (tuple(ids_generos), id_libro))
        libros_similares = cur.fetchall()

        # Verificar si se encontraron libros similares
        if not libros_similares:
            return jsonify({'message': 'No se encontraron libros similares'}), 404
        
        # Respuesta de éxito
        return jsonify(libros_similares), 200
    except Exception as err:
        print(f"Error al obtener libros similares: {err}")
        return jsonify({'message': f'Error interno del servidor: {str(err)}'}), 500
    finally:
        # Cerrar el cursor
        if cur: cur.close()

# Obtener la calificacion que un usuario le ha dado a un libro
@book_bp.route('/book/<int:id_libro>/rating/<int:id_usuario>', methods=['GET'])
def getUserRating(id_libro, id_usuario):
    from app import mysql
    cur = None
    try:
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Consultar la calificación del usuario para el libro
        cur.execute("SELECT puntaje FROM Calificacion_Usuario WHERE id_usuario = %s AND id_libro = %s", (id_usuario, id_libro))
        calificacion = cur.fetchone()

        # Verificar si se encontró la calificación
        if not calificacion:
            return jsonify({'message': 'No se encontró la calificación del usuario para este libro'}), 404
        
        return jsonify({'puntaje': calificacion['puntaje']}), 200
    except Exception as err:
        print(f"Error al obtener la calificación del usuario: {err}")
        return jsonify({'message': f'Error interno del servidor: {str(err)}'}), 500
    finally:
        if cur: cur.close()

# Obtener cantidad de calificaciones de un libro
@book_bp.route('/book/<int:id_libro>/ratings/count', methods=['GET'])
def getBookRatingCount(id_libro):
    from app import mysql
    cur = None
    try:
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Consultar la cantidad de calificaciones del libro
        cur.execute("SELECT COUNT(*) as count FROM Calificacion_Usuario WHERE id_libro = %s", (id_libro,))
        count = cur.fetchone()

        # Verificar si se encontró la cantidad de calificaciones
        if not count:
            return jsonify({'message': 'No se encontraron calificaciones para este libro'}), 404
        
        return jsonify({'count': count['count']}), 200
    except Exception as err:
        print(f"Error al obtener la cantidad de calificaciones del libro: {err}")
        return jsonify({'message': f'Error interno del servidor: {str(err)}'}), 500
    finally:
        if cur: cur.close()

# Calificar un libro
@book_bp.route('/book/<int:id_libro>/rate', methods=['POST'])
def rateBook(id_libro):
    from app import mysql
    cur = None
    try:
        # Obtener la conexión a la base de datos
        cur = mysql.connection.cursor()

        # Obtener los datos de la calificación
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        puntaje = data.get('puntaje')

        # Verificar si el usuario ha calificado el libro antes
        cur.execute("SELECT puntaje FROM Calificacion_Usuario WHERE id_usuario = %s AND id_libro = %s", (id_usuario, id_libro))

        # Si el usuario ya ha calificado el libro, actualizar la calificación
        if cur.rowcount > 0:
            cur.execute("UPDATE Calificacion_Usuario SET puntaje = %s WHERE id_usuario = %s AND id_libro = %s", (puntaje, id_usuario, id_libro))
        else:
            # Si el usuario no ha calificado el libro, insertar una nueva calificación
            cur.execute("INSERT INTO Calificacion_Usuario (id_usuario, id_libro, puntaje) VALUES (%s, %s, %s)", (id_usuario, id_libro, puntaje))
        
        # Calcular el nuevo promedio de calificaciones del libro
        cur.execute("SELECT AVG(puntaje) as promedio FROM Calificacion_Usuario WHERE id_libro = %s", (id_libro,))
        resultado = cur.fetchone()

        # Actualizar la calificación del libro
        cur.execute("UPDATE libro SET promedio = %s WHERE id_libro = %s", (resultado['promedio'], id_libro))
        mysql.connection.commit()

        return jsonify({'message': 'Calificación actualizada correctamente'}), 200
    except Exception as err:
        print(f"Error al calificar el libro: {err}")
        return jsonify({'message': f'Error interno del servidor: {str(err)}'}), 500


# Actualizar un libro por su ID
@book_bp.route('/book/edit/<int:id_libro>', methods=['PATCH'])
def updateBook(id_libro):
    from app import mysql
    cur = None
    try:
        data = request.get_json()
        # Campos según modelo
        campos = [
            'titulo', 'autor', 'artista', 'anio_publicacion', 'portada', 'estado',
            'link_compra', 'editorial', 'idioma', 'es_saga',
            'titulo_saga', 'num_libro', 'num_capitulos', 'sinopsis'
        ]
        valores = [data.get(campo) for campo in campos]
        set_clause = ', '.join([f"{campo}=%s" for campo in campos])

        cur = mysql.connection.cursor()
        cur.execute(
            f"UPDATE libro SET {set_clause} WHERE id_libro = %s",
            (*valores, id_libro)
        )
        mysql.connection.commit()
        
        # Registrar la edición del libro
        id_usuario = data.get('id_usuario')
        if id_usuario:
            tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur.execute(
                "INSERT INTO Edicion (id_libro, id_usuario, tiempo) VALUES (%s, %s, %s)",
                (id_libro, id_usuario, tiempo)
            )
            mysql.connection.commit()
        return jsonify({'message': 'Libro actualizado correctamente'}), 200
    except Exception as err:
        print(f"Error al actualizar el libro: {err}")
        return jsonify({'message': f'Error interno del servidor: {err}'}), 500
    finally:
        if cur: cur.close()


#Edicion libro por id
@book_bp.route('/book/<int:id_libro>/edit-history', methods=['GET'])
def get_edit_history(id_libro):
    from app import mysql
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT e.tiempo, u.nombre_usuario
            FROM edicion e
            JOIN usuario u ON e.id_usuario = u.id_usuario
            WHERE e.id_libro = %s
            ORDER BY e.tiempo DESC
        """, (id_libro,))
        rows = cur.fetchall()
        historial = [{'tiempo': row['tiempo'], 'nombre_usuario': row['nombre_usuario']} for row in rows]
        return jsonify({'historial': historial}), 200
    except Exception as e:
        print(f"Error al obtener historial de ediciones: {e}")
        return jsonify({'error': 'Error interno'}), 500
    finally:
        cur.close()