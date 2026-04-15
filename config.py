import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (solo para desarrollo local)
load_dotenv()

class Config:
    """Configuración principal de la aplicación"""
    
    # =====================================================
    # CONEXIÓN A POSTGRESQL EN RENDER
    # =====================================================
    # Completa con tus datos de Render:
    username = "odoo_user"
    password = "heaprQrLZYNgcJZx0DQcDfleqn9MuOKP"
    host = "dpg-d7b6k4cvjg8s73etr2ng-a.frankfurt-postgres.render.com"
    port = "5432"
    database = "odoo_clone"
    
    # Construir URL de conexión con SSL requerido
    url_bd_render = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode=require"
    
    # Variable de entorno DATABASE_URL (prioritaria) o usar la URL construida
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', url_bd_render)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # =====================================================
    # CONFIGURACIÓN DE SEGURIDAD
    # =====================================================
    # Clave secreta (en producción usar variable de entorno)
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-para-desarrollo-2026')
    
    # =====================================================
    # OTRAS CONFIGURACIONES
    # =====================================================
    DEBUG = True  
    PORT = int(os.getenv('PORT', 5000))