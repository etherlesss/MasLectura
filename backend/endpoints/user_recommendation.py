from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os
from ai.recommend import getRecommendations

# Crear un objeto Blueprint para la ruta de recomendaciones de usuario
user_recommendation_bp = Blueprint('user-recommendation', __name__)

@user_recommendation_bp.route('/recommend', methods=['GET'])
def recommend():
    if not os.path.exists('model/xgboost_model.pkl'):
        return jsonify({'error': 'Modelo no encontrado'}), 404

    # Cargar modelo y datos
    model = joblib.load('model/xgboost_model.pkl')
    user_embeddings = np.load('model/user_embeddings.npy')
    book_embeddings = np.load('model/book_embeddings.npy')
    user_ids = np.load('model/user_ids.npy')
    book_ids = np.load('model/book_ids.npy')
    genres_onehot = pd.read_csv('model/genres_onehot.csv', index_col=0)
    tags_onehot = pd.read_csv('model/tags_onehot.csv', index_col=0)

    user_id = request.args.get('id_usuario', type=int)
    recs = getRecommendations(
        user_id, model, user_embeddings, book_embeddings, user_ids, book_ids, genres_onehot, tags_onehot, top_n=10
    )

    return jsonify([{'id_libro': r[0], 'score': float(r[1])} for r in recs])
