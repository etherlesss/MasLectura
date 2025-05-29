import numpy as np

# Extrae los favoritos de un usuario con una calificación mínima.
def getUserFavorites(user_id, min_rating=4):
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT lg.id_genero, le.id_etiquetas
            FROM Calificacion_Usuario cu
            LEFT JOIN Libro_Genero lg ON cu.id_libro = lg.id_libro
            LEFT JOIN Libro_Etiquetas le ON cu.id_libro = le.id_libro
            WHERE cu.id_usuario = %s AND cu.puntaje >= %s
        """, (user_id, min_rating))
        data = cur.fetchall()

        # print("Favoritos:", data)

        # Set para evitar duplicados
        generos = set()
        etiquetas = set()

        # Recorrer los resultados y agregar a los sets
        for row in data:
            if row['id_genero']: generos.add(row['id_genero'])
            if row['id_etiquetas']: etiquetas.add(row['id_etiquetas'])
        return list(generos), list(etiquetas)
    except Exception as err:
        print(f"Error al obtener los favoritos del usuario {user_id}: {err}")
    finally:
        if cur: cur.close()

# Obtiene los candidatos recomendados basados en géneros y etiquetas favoritas.
def getCandidates(fav_genres, fav_tags):
    from app import mysql
    cur = None
    try:
        cur = mysql.connection.cursor()
        # Si no hay favoritos, pon un valor imposible
        if not fav_genres:
            fav_genres = [-1]
        if not fav_tags:
            fav_tags = [-1]
        # Construir placeholders dinámicamente
        genre_placeholders = ','.join(['%s'] * len(fav_genres))
        tag_placeholders = ','.join(['%s'] * len(fav_tags))

        # print(f"Buscando candidatos para géneros={fav_genres}, etiquetas={fav_tags}")

        # print("PARAMS:", tuple(fav_genres) + tuple(fav_tags))
        # total_placeholders = genre_placeholders.count('%s') + tag_placeholders.count('%s')
        # total_params = len(tuple(fav_genres) + tuple(fav_tags))
        # print(f"Placeholders: {total_placeholders}, Params: {total_params}")

        query = (
            "SELECT DISTINCT l.id_libro "
            "FROM Libro l "
            "LEFT JOIN Libro_Genero lg ON l.id_libro = lg.id_libro "
            "LEFT JOIN Libro_Etiquetas le ON l.id_libro = le.id_libro "
            f"WHERE lg.id_genero IN ({genre_placeholders}) OR le.id_etiquetas IN ({tag_placeholders})"
        )
        cur.execute(query, tuple(fav_genres) + tuple(fav_tags))

        books = [row['id_libro'] for row in cur.fetchall()]
        
        # print(f"Candidatos encontrados: {books}")
        return books
    except Exception as err:
        print(f"Error al obtener los candidatos recomendados: {err}")
    finally:
        if cur: cur.close()

# Recomienda libros a un usuario basado en un modelo y filtrando por géneros/etiquetas favoritos.
def getRecommendations(user_id, model, user_embeddings, book_embeddings, user_ids, book_ids, genres_onehot, tags_onehot, top_n=5):
    fav_genres, fav_tags = getUserFavorites(user_id)
    candidates = getCandidates(fav_genres, fav_tags)
    if not candidates:
        print(f"No hay candidatos recomendados para el usuario {user_id}.")
        return []
    
    # Buscar el indice del usuario
    if user_id not in user_ids:
        print(f"El usuario {user_id} no está en el modelo.")
        return []
    user_idx = np.where(user_ids == user_id)[0][0]

    # Predecir para cada libro candidato
    pred = []
    for book_id in candidates:
        if book_id not in book_ids:
            continue
        book_idx = np.where(book_ids == book_id)[0][0]
        genre_vec = genres_onehot.loc[book_id].values if book_id in genres_onehot.index else np.zeros(genres_onehot.shape[1])
        tag_vec = tags_onehot.loc[book_id].values if book_id in tags_onehot.index else np.zeros(tags_onehot.shape[1])
        features = np.concatenate([user_embeddings[user_idx], book_embeddings[book_idx], genre_vec, tag_vec])
        pred_score = model.predict(features.reshape(1, -1))[0]
        pred.append((book_id, pred_score))

    # Ordenar y devolver los top_n
    pred.sort(key=lambda x: x[1], reverse=True)
    return pred[:top_n]