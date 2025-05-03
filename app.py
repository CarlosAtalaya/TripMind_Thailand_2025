import os
from flask import Flask, render_template, jsonify, request
from services.itinerary import load_itinerary, get_current_region
from services.weather import get_weather_for_region
from services.news import get_filtered_news
from datetime import datetime
import pytz
from services import format_date

app = Flask(__name__)

# Configuración básica
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_mvp')

# Registrar filtros personalizados
app.jinja_env.filters['format_date'] = format_date

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

# Añadir esta nueva ruta en app.py
@app.route('/api/news/all')
def get_all_news():
    """API para obtener todas las noticias relevantes para el viaje"""
    max_items = request.args.get('max', 20, type=int)
    itinerary_name = request.args.get('itinerary', 'thailand_2025.yaml')
    
    # Obtener noticias relevantes
    news_data = get_filtered_news(itinerary_name, max_items)
    
    return jsonify({
        'articles': news_data
    })

if __name__ == '__main__':
    app.run(debug=True)
