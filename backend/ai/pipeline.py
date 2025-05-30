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

# Cargar dataset amazon para training
def getAmazonRatingsDF():
    max_users = 10000
    max_books = 10000
    books_amzn = pd.read_csv('ai/training/books_data.csv')
    reviews_amzn = pd.read_csv('ai/training/Books_rating.csv')
    id_offset = 1000000
    reviews_amzn = reviews_amzn.rename(columns={
        'User_id': 'id_usuario',
        'Title': 'titulo',
        'review/score': 'puntaje'
    })
    books_amzn['id_libro'] = books_amzn['Title'].astype('category').cat.codes + id_offset
    reviews_amzn = reviews_amzn.merge(books_amzn[['Title', 'id_libro']], left_on='titulo', right_on='Title', how='left')
    df_amzn = reviews_amzn[['id_usuario', 'id_libro', 'puntaje']].dropna()
    df_amzn['puntaje'] = pd.to_numeric(df_amzn['puntaje'], errors='coerce')
    df_amzn = df_amzn.dropna(subset=['puntaje'])

    # Filtrar por los usuarios y libros más frecuentes
    top_users = df_amzn['id_usuario'].value_counts().nlargest(max_users).index
    top_books = df_amzn['id_libro'].value_counts().nlargest(max_books).index
    df_amzn = df_amzn[df_amzn['id_usuario'].isin(top_users) & df_amzn['id_libro'].isin(top_books)]

    return df_amzn

# Combinar dataframes
def getCombinedRatingsDF(use_local, use_amazon):
    dfs = []
    if use_local:
        df_local = getRatingsDataframe()
        if df_local is not None:
            dfs.append(df_local)
    if use_amazon:
        df_amzn = getAmazonRatingsDF()
        if df_amzn is not None:
            dfs.append(df_amzn)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return None

# Construye una matriz de utilidad (usuarios x libros) a partir del DataFrame de calificaciones.
def buildUtiltyMatrix(df):
    # Eliminar duplicados (multiples calificaciones de un usuario a un libro)
    df = df.drop_duplicates(subset=['id_usuario', 'id_libro'], keep='last')
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