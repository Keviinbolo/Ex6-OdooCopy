from flask import Flask, redirect, url_for
from flask_login import LoginManager
from sqlalchemy import inspect, text
import os
from config import Config
from models import db, User

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario por ID para Flask-Login"""
    return User.query.get(int(user_id))

# Registrar blueprints (rutas)
from auth import auth_bp
from contacts import contacts_bp

app.register_blueprint(auth_bp)
app.register_blueprint(contacts_bp)

# Ruta principal
@app.route('/')
def index():
    """Redirigir a login o apps según autenticación"""
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for('contacts.apps'))
    return redirect(url_for('auth.login'))

# Crear tablas al iniciar (solo primera vez)
with app.app_context():
    db.create_all()

    # Crear carpeta de uploads para iconos de contacto.
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads', 'contacts'), exist_ok=True)

    # Si la tabla ya existia, agregar columna photo cuando falte.
    inspector = inspect(db.engine)
    if 'contacts' in inspector.get_table_names():
        existing_columns = {column['name'] for column in inspector.get_columns('contacts')}
        if 'photo' not in existing_columns:
            db.session.execute(text('ALTER TABLE contacts ADD COLUMN photo VARCHAR(255)'))
            db.session.commit()

    print(" Base de datos inicializada correctamente")
    print(f" Conectado a: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT)