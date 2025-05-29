'''
    PIPELINE, PARA MANEJAR LOS PASOS DE LA IA
'''
import pandas as pd

# Extrae los datos de las calificaciones de la base de datos y devuelve un DataFrame.
def getRatingsDataframe():
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usuario, id_libro, puntaje FROM Calificacion_Usuario")
        data = cur.fetchall()
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data, columns=['id_usuario', 'id_libro', 'puntaje'])

        # print("Datos de calificaciones obtenidos:", df.head())

        return df
    except Exception as err:
        print(f"Error al obtener los datos de calificaciones: {err}")
    finally:
        if cur: cur.close()

# Obtiene los géneros de los libros en formato one-hot encoding.
'''
    One hot encoding convierte cada género en una columna binaria, donde 1 indica que el libro pertenece a ese género y 0 indica que no.
'''
def getGenresOneHot():
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_libro, id_genero FROM Libro_Genero")
        data = cur.fetchall()
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data, columns=['id_libro', 'id_genero'])
        # Obtener todos los géneros únicos
        all_genres = df['id_genero'].unique()
        # Crear columnas one-hot encoding para cada género
        one_hot = pd.DataFrame(0, index=df['id_libro'].unique(), columns=all_genres)
        for _, row in df.iterrows():
            one_hot.at[row['id_libro'], row['id_genero']] = 1
        # Devolver el DataFrame one-hot
        return one_hot
    except Exception as err:
        print(f"Error al obtener los géneros de los libros: {err}")
    finally:
        if cur: cur.close()

# Obtiene las etiquetas de los libros en formato one-hot encoding.
def getTagsOneHot():
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_libro, id_etiquetas FROM Libro_Etiquetas")
        data = cur.fetchall()
        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame(data, columns=['id_libro', 'id_etiquetas'])
        # Obtener todas las etiquetas únicas
        all_tags = df['id_etiquetas'].unique()
        # Crear columnas one-hot encoding para cada etiqueta
        one_hot = pd.DataFrame(0, index=df['id_libro'].unique(), columns=all_tags)
        for _, row in df.iterrows():
            one_hot.at[row['id_libro'], row['id_etiquetas']] = 1
        # Devolver el DataFrame one-hot
        return one_hot
    except Exception as err:
        print(f"Error al obtener las etiquetas de los libros: {err}")
    finally:
        if cur: cur.close()

# Construye una matriz de utilidad (usuarios x libros) a partir del DataFrame de calificaciones.
def buildUtiltyMatrix(df):
    # Pivotear el DataFrame para crear la matriz de utilidad
    matrix = df.pivot(index='id_usuario', columns='id_libro', values='puntaje')
    # Rellenar los valores NaN con 0, libros que no han sido calificados por un usuario
    matrix = matrix.fillna(0)
    
    # print("Matriz de utilidad construida:", matrix.head())

    return matrix

# Centrar la matriz de utilidad restando la media de cada fila (usuario)
def centerUtilityMatrix(matrix):
    # Calcular la media de cada fila (usuario)
    userMeans = matrix.mean(axis=1)
    # Restar la media de cada fila
    centeredMatrix = matrix.sub(userMeans, axis=0)
    
    # print("Matriz de utilidad centrada:", centeredMatrix.head())

    return centeredMatrix, userMeans