import numpy as np
import joblib
import os
from sklearn.model_selection import GridSearchCV
from ai.pipeline import getRatingsDataframe, buildUtiltyMatrix, centerUtilityMatrix, getGenresOneHot, getTagsOneHot
from ai.svd import trainSVD
from ai.xgboost_model import buildXGBDataset, trainXGB
from app import app

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

with app.app_context():
    df = getRatingsDataframe()
    genres_onehot = getGenresOneHot()
    tags_onehot = getTagsOneHot()
    if df is not None:
        matrix = buildUtiltyMatrix(df)
        centered_matrix, user_means = centerUtilityMatrix(matrix)
        svd, user_embeddings, book_embeddings = trainSVD(centered_matrix, n_components=30)
        user_ids = matrix.index.values
        book_ids = matrix.columns.values
        X, y = buildXGBDataset(df, user_embeddings, book_embeddings, user_ids, book_ids, genres_onehot, tags_onehot)
        
        # Separar en train y test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # USAR EL CÓDIGO COMENTADO PARA OPTIMIZAR LOS HIPERPARÁMETROS DEL MODELO XGB
        '''
        # Definir el modelo base
        xgb_model = xgb.XGBRegressor(random_state=42)

        # Definir hiperparámetros
        param_grid = {
            'n_estimators': [300, 550, 800],
            'max_depth': [3, 4, 5],
            'learning_rate': [0.1, 0.05, 0.01]
        }

        # Configurar GridSearchCV
        grid_search = GridSearchCV(
            estimator=xgb_model,
            param_grid=param_grid,
            scoring='neg_mean_squared_error',
            cv=3,
            verbose=2,
            n_jobs=-1
        )

        # Ejecutar el grid search
        grid_search.fit(X_train, y_train)

        print("Mejores hiperparámetros encontrados:")
        print(grid_search.best_params_)
        print("Mejor score (neg MSE):", grid_search.best_score_)

        # Usa el mejor modelo encontrado
        model = grid_search.best_estimator_
        '''

        # Entrenar modelo con datos de entrenamiento
        model = trainXGB(X_train, y_train)

        # Crear carpeta para guardar el modelo si no existe
        os.makedirs('model', exist_ok=True)

        # Guardar el modelo entrenado
        joblib.dump(model, 'model/xgboost_model.pkl')

        # Guardar embeddings
        np.save('model/user_embeddings.npy', user_embeddings)
        np.save('model/book_embeddings.npy', book_embeddings)
        np.save('model/user_ids.npy', user_ids)
        np.save('model/book_ids.npy', book_ids)

        # Guardar one-hots
        genres_onehot.to_csv('model/genres_onehot.csv')
        tags_onehot.to_csv('model/tags_onehot.csv')

        # Evaluar el modelo
        y_pred = model.predict(X_test)
        print(f"MSE (test): {mean_squared_error(y_test, y_pred)} - Mean Squared Error; Mientras mas bajo, mejor.")
        print(f"MAE (test): {mean_absolute_error(y_test, y_pred)} - Mean Absolute Error; En promedio, cuanto se desvía la predicción del valor real. Mientras mas bajo, mejor.")
        print(f"R2 (test): {r2_score(y_test, y_pred)} - Coeficiente de determinación; Entre -inf y 1, mientras mas alto, mejor. Equivale al porcentaje de varianza explicada por el modelo. Mientras mas cerca de 0, peor es el modelo, ya que predice la media.")

        # Mostrar predicciones
        print("\nAlgunas predicciones (real vs predicho):")
        for i in range(min(10, len(y_test))):
            print(f"Real: {y_test[i]:.2f} - Predicho: {y_pred[i]:.2f}")

        # Importancia de los features
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        # Dar nombre a las features
        feature_names = (
            [f"user_emb_{i}" for i in range(user_embeddings.shape[1])] +
            [f"book_emb_{i}" for i in range(book_embeddings.shape[1])] +
            [f"genre_{g}" for g in genres_onehot.columns] +
            [f"tag_{t}" for t in tags_onehot.columns]
        )

        # Mostrar las 20 features más importantes
        print("Top 20 features más importantes:")
        for i in range(20):
            idx = indices[i]
            print(f"{feature_names[idx]}: importancia {importances[idx]:.4f}")
        