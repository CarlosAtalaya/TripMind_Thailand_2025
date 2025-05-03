import requests
from datetime import datetime, timedelta
import os
from config import OPENMETEO_API_URL

def get_weather_for_region(region, days=3):
    """
    Obtiene el pronóstico del tiempo para una región específica
    
    Args:
        region: Datos de la región (debe incluir lat/long o nombre)
        days: Número de días para el pronóstico
        
    Returns:
        dict: Datos del clima
    """
    try:
        # Priorizar coordenadas exactas si están disponibles
        if 'latitude' in region and 'longitude' in region:
            lat = region['latitude']
            lon = region['longitude']
        else:
            # Si no hay coordenadas, intentar geocodificar el nombre de la región
            lat, lon = geocode_region(region['name'])
        
        # Si no se pudieron obtener coordenadas, devolver error
        if not lat or not lon:
            return {'error': 'No se pudieron determinar las coordenadas de la región'}
        
        # Configurar parámetros para OpenMeteo
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode',
            'timezone': 'auto',
            'forecast_days': days
        }
        
        response = requests.get(OPENMETEO_API_URL, params=params)
        data = response.json()
        
        # Procesar y formatear los datos del clima para facilitar su uso en el frontend
        processed_data = {
            'region': region['name'],
            'forecast': []
        }
        
        # Asumiendo que daily tiene los datos por día
        if 'daily' in data:
            daily = data['daily']
            for i in range(len(daily.get('time', []))):
                day_data = {
                    'date': daily['time'][i],
                    'temp_max': daily['temperature_2m_max'][i],
                    'temp_min': daily['temperature_2m_min'][i],
                    'precipitation': daily['precipitation_sum'][i],
                    'weather_code': daily['weathercode'][i],
                    'weather_description': get_weather_description(daily['weathercode'][i])
                }
                processed_data['forecast'].append(day_data)
        
        return processed_data
    except Exception as e:
        print(f"Error al obtener el clima: {e}")
        return {'error': 'Error al obtener datos del clima', 'message': str(e)}

def geocode_region(region_name):
    """
    Obtiene las coordenadas de una región por su nombre
    
    Args:
        region_name: Nombre de la región
        
    Returns:
        tuple: (latitud, longitud)
    """
    try:
        # URL del servicio de geocodificación (podría ser Nominatim o similar)
        geocode_url = "https://nominatim.openstreetmap.org/search"
        
        params = {
            'q': region_name,
            'format': 'json',
            'limit': 1
        }
        
        headers = {
            'User-Agent': 'TravelBoard/0.1'  # Importante para respetar los términos de uso
        }
        
        response = requests.get(geocode_url, params=params, headers=headers)
        data = response.json()
        
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None, None
    except Exception as e:
        print(f"Error al geocodificar: {e}")
        return None, None

def get_weather_description(code):
    """
    Convierte el código de clima de OpenMeteo en una descripción legible
    
    Args:
        code: Código numérico del clima
        
    Returns:
        str: Descripción del clima
    """
    # Mapeo básico de códigos a descripciones según OpenMeteo
    weather_codes = {
        0: 'Cielo despejado',
        1: 'Mayormente despejado',
        2: 'Parcialmente nublado',
        3: 'Nublado',
        45: 'Niebla',
        48: 'Niebla con escarcha',
        51: 'Llovizna ligera',
        53: 'Llovizna moderada',
        55: 'Llovizna intensa',
        61: 'Lluvia ligera',
        63: 'Lluvia moderada',
        65: 'Lluvia intensa',
        71: 'Nevada ligera',
        73: 'Nevada moderada',
        75: 'Nevada intensa',
        80: 'Chubascos ligeros',
        81: 'Chubascos moderados',
        82: 'Chubascos intensos',
        95: 'Tormenta eléctrica',
        96: 'Tormenta con granizo ligero',
        99: 'Tormenta con granizo intenso'
    }
    
    return weather_codes.get(code, 'Desconocido')