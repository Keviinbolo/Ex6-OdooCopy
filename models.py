from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Crear instancia de SQLAlchemy (se inicializará en app.py)
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de Usuario"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # En producción: usar hash
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relación con contactos
    contacts = db.relationship('Contact', backref='owner', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Contact(db.Model):
    """Modelo de Contacto"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Clave foránea
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Contact {self.name}>'
    
    def to_dict(self):
        """Convertir contacto a diccionario (para APIs)"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'position': self.position,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }