from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload_image', __name__)

UPLOAD_FOLDER = 'uploads'

@upload_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'imagen' not in request.files:
        return jsonify({'message': 'No se envió ninguna imagen'}), 400
    file = request.files['imagen']
    if file.filename == '':
        return jsonify({'message': 'Nombre de archivo vacío'}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    # Devuelve la URL pública
    url = f'/uploads/{filename}'
    return jsonify({'url': url}), 201

# Para servir archivos estáticos
@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)