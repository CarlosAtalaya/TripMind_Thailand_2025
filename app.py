import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, current_user
from services.itinerary import load_itinerary, get_current_region
from services.weather import get_weather_for_region
from services.news import get_filtered_news
from datetime import datetime
import pytz
from services import format_date
from votes import initialize_categories
from models import db, User
from auth import auth
from files import files
from votes import votes
from diary import diary
from poop_counter import poop_counter
from daily_photos import daily_photos  # Nuevo import
import logging
from logging.handlers import RotatingFileHandler
from config import MAX_UPLOAD_SIZE

app = Flask(__name__)

# Configuración básica
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_mvp')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tripboard.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE  # Usar el límite configurado

# Configuración de logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/tripboard.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('TripBoard startup')
# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

# Función ahora para plantillas
@app.template_filter('now')
def get_now():
    return datetime.now()

# Registrar filtros personalizados
app.jinja_env.filters['format_date'] = format_date
app.jinja_env.globals['now'] = get_now

# Registrar blueprint de autenticación
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(files, url_prefix='/files')
app.register_blueprint(votes, url_prefix='/votes')
app.register_blueprint(diary, url_prefix='/diary')
app.register_blueprint(poop_counter)
app.register_blueprint(daily_photos)  # Registrar el nuevo blueprint

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Middleware para verificar configuración inicial
@app.before_request
def check_initial_setup():
    # Rutas que siempre deben estar accesibles
    public_endpoints = ['static', 'setup', 'auth.login', 'auth.logout']
    
    # Si estamos en una ruta pública, permitir acceso
    if request.endpoint in public_endpoints:
        return None
        
    # Verificar si hay usuarios en la base de datos
    user_count = User.query.count()
    if user_count == 0 and request.endpoint != 'setup':
        # Si no hay usuarios y no estamos en setup, redirigir a setup
        return redirect(url_for('setup'))
        
    # Verificar si el usuario está autenticado para rutas protegidas
    if not current_user.is_authenticated and request.endpoint not in public_endpoints:
        return redirect(url_for('auth.login'))

@app.route('/')
def index():
    """Página principal que muestra el resumen del itinerario"""
    # Por ahora cargamos un itinerario por defecto
    itinerary = load_itinerary('thailand_2025.yaml')

    # Verificar que itinerary tiene la propiedad regions y que no es None
    if 'regions' not in itinerary or itinerary['regions'] is None:
        itinerary['regions'] = []
    
    # Determinar la región actual basada en la fecha
    current_date = datetime.now(pytz.UTC)
    current_region = get_current_region(itinerary, current_date)
    
    return render_template('index.html', 
                          itinerary=itinerary, 
                          current_date=current_date,
                          current_region=current_region)

@app.route('/itinerary')
def itinerary_view():
    """Vista detallada del itinerario"""
    itinerary_name = request.args.get('name', 'thailand_2025.yaml')
    itinerary = load_itinerary(itinerary_name)
    
    # Determinar la región actual basada en la fecha
    current_date = datetime.now(pytz.UTC)
    current_region = get_current_region(itinerary, current_date)
    
    return render_template('itinerary.html',
                          itinerary=itinerary,
                          current_date=current_date,
                          current_region=current_region)

@app.route('/api/itinerary')
def get_itinerary():
    """API para obtener el itinerario completo"""
    itinerary_name = request.args.get('name', 'thailand_2025.yaml')
    itinerary = load_itinerary(itinerary_name)
    return jsonify(itinerary)

@app.route('/api/weather/<region_id>')
def get_weather(region_id):
    """API para obtener el clima de una región específica"""
    days = request.args.get('days', 3, type=int)
    itinerary = load_itinerary('thailand_2025.yaml')
    
    # Encontrar la región en el itinerario
    region = next((r for r in itinerary['regions'] if r['id'] == region_id), None)
    
    if not region:
        return jsonify({'error': 'Región no encontrada'}), 404
    
    # Obtener clima usando coordenadas o nombre de la región
    weather_data = get_weather_for_region(region, days)
    return jsonify(weather_data)

@app.route('/api/news/all')
def get_all_news():
    """API para obtener todas las noticias relevantes para el viaje"""
    max_items = request.args.get('max', 50, type=int)
    itinerary_name = request.args.get('itinerary', 'thailand_2025.yaml')
    
    # Obtener noticias relevantes
    news_data = get_filtered_news(itinerary_name, max_items)
    
    return jsonify({
        'articles': news_data
    })

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Página de configuración inicial para crear el primer usuario admin"""
    # Comprobar si ya existen usuarios
    user_count = User.query.count()
    
    if user_count > 0:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        # Crear usuario administrador
        admin = User(username=username, name=name, phone=phone, is_admin=True)
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"Usuario administrador creado: {username}")
        return redirect(url_for('auth.login'))
        
    current_date = datetime.now(pytz.UTC)
    return render_template('setup.html', current_date=current_date)

# Crear tablas de la base de datos
def create_tables():
    """Crear tablas de la base de datos"""
    with app.app_context():
        db.create_all()
        print("Tablas de la base de datos creadas.")
        
        initialize_categories()
        print("Categorías de votación inicializadas.")

if __name__ == '__main__':
    # Crear tablas antes de iniciar la aplicación
    create_tables()
    app.run(host='192.168.1.230', port=5000, debug=True)