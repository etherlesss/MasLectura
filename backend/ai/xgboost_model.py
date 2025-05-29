import numpy as np
import xgboost as xgb
import pandas as pd

# Extrae los datos de las calificaciones de la base de datos y devuelve un DataFrame.
def buildXGBDataset(df, userEmbeddings, bookEmbeddings, userIDs, bookIDs, genres_onehot, tags_onehot):
    X = [] # Features
    y = [] # Labels
    # Iterar sobre cada fila del DataFrame
    for _, row in df.iterrows():
        user_idx = np.where(userIDs == row['id_usuario'])[0][0] # Obtener el índice del usuario
        book_idx = np.where(bookIDs == row['id_libro'])[0][0] # Obtener el índice del libro
        genre_vec = genres_onehot.loc[row['id_libro']].values if row['id_libro'] in genres_onehot.index else np.zeros(genres_onehot.shape[1])
        tag_vec = tags_onehot.loc[row['id_libro']].values if row['id_libro'] in tags_onehot.index else np.zeros(tags_onehot.shape[1])
        features = np.concatenate([userEmbeddings[user_idx], bookEmbeddings[book_idx], genre_vec, tag_vec]) # Concatenar los embeddings del usuario y del libro
        X.append(features) # Agregar las features
        y.append(row['puntaje']) # Agregar la etiqueta (puntaje)

    # Convertir a array de numpy
    X = np.array(X) 
    y = np.array(y)
    print("X shape:", X.shape)  # Mostrar la forma de X
    print("y shape:", y.shape)  # Mostrar la forma de y
    return X, y

# Entrenar un modelo XGBoost con los embeddings de usuarios y libros.
def trainXGB(X, y):
    # Definir los parámetros del modelo XGBoost
    '''
        n_estimators: Número de árboles en el modelo.
        max_depth: Profundidad máxima de los árboles.
        learning_rate: Tasa de aprendizaje para actualizar los pesos.
        random_state: Semilla para la aleatoriedad, para reproducibilidad.
    '''
    model = xgb.XGBRegressor(n_estimators=800, max_depth=3, learning_rate=0.1, random_state=42)
    model.fit(X, y)  # Entrenar el modelo
    print("Modelo XGBoost entrenado.")
    return model