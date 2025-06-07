from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

upload_foto_perfil_bp = Blueprint('upload_foto_perfil', __name__)

UPLOADS_PERFIL = os.path.join(os.getcwd(), 'uploads_perfil')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOADS_PERFIL, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_foto_perfil_bp.route('/upload_foto_perfil', methods=['POST'])
def upload_foto_perfil():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOADS_PERFIL, filename)
        file.save(save_path)
        url = f"/uploads_perfil/{filename}"
        return jsonify({'filename': filename, 'url': url}), 201
    return jsonify({'error': 'File type not allowed'}), 400

@upload_foto_perfil_bp.route('/uploads_perfil/<filename>')
def uploaded_profile_pic(filename):
    return send_from_directory(UPLOADS_PERFIL, filename)