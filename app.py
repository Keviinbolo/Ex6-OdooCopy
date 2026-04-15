from flask import Flask, redirect, url_for
from flask_login import LoginManager
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
    print(" Base de datos inicializada correctamente")
    print(f" Conectado a: {Config.SQLALCHEMY_DATABASE_URI[:50]}...")

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT)