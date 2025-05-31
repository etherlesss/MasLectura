# Importar dependencias
from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Importar base de datos
from db import init_mysql

# Importar rutas
from routes.login import login_bp
from routes.signup import signup_bp
from routes.profile import profile_bp
from routes.genre import genre_bp
from routes.tag import tag_bp
from routes.book import book_bp
from routes.book_tag import book_tag_bp
from routes.book_genre import book_genre_bp  
from routes.upload_image import upload_bp
from routes.list import list_bp
from routes.comment import comment_bp
from routes.user import user_bp

# Importar endpoints
from endpoints.recoverpwd import recover_password_bp
from endpoints.user_recommendation import user_recommendation_bp

# Cargar variables de entorno
load_dotenv()

# Definir variables
PORT = os.getenv("PORT") or 5000
# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar CORS
cors_config = {
    "origins" : "*",
    "methods" : ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
}
CORS(app, resources={r"/*": cors_config})

# Inicializar Flask-Mail
mail = Mail()

# Configurar Flask-Mail
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

# Configurar el remitente del correo
mail.init_app(app)

# Inicializar la base de datos
mysql = init_mysql(app)

# Probar la conexión a la base de datos
@app.route('/test_db', methods=['GET'])
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT VERSION()")
        db_version = cur.fetchone()
        return jsonify({"db_version": db_version}), 200
    except Exception as err:
        print(f"Error al conectar a la base de datos: {err}")
        return jsonify({"error": "Error al conectar a la base de datos"}), 500
    finally:
        cur.close()

# Registrar blueprints
app.register_blueprint(login_bp, url_prefix='/api')
app.register_blueprint(signup_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api')
app.register_blueprint(recover_password_bp, url_prefix='/api')
app.register_blueprint(genre_bp, url_prefix='/api')
app.register_blueprint(tag_bp, url_prefix='/api')
app.register_blueprint(book_bp, url_prefix='/api')
app.register_blueprint(book_tag_bp, url_prefix='/api')
app.register_blueprint(book_genre_bp, url_prefix='/api')
app.register_blueprint(upload_bp, url_prefix='/api')
app.register_blueprint(list_bp, url_prefix='/api')
app.register_blueprint(comment_bp, url_prefix='/api')
app.register_blueprint(user_recommendation_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

# Mensaje de encendido del servidor backend
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)