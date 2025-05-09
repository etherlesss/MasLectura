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

# Importar endpoints
from endpoints.recoverpwd import recover_password_bp

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

# Mensaje de encendido del servidor backend
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=True)