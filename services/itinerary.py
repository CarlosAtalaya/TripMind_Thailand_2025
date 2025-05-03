import os
import yaml
from datetime import datetime
import pytz

def load_itinerary(filename):
    """
    Carga un itinerario desde un archivo YAML
    
    Args:
        filename: Nombre del archivo YAML en la carpeta data/itineraries/
        
    Returns:
        dict: Datos del itinerario
    """
    try:
        file_path = os.path.join('data', 'itineraries', filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            itinerary = yaml.safe_load(file)
            
        # Convertir fechas principales del itinerario
        if 'start_date' in itinerary:
            itinerary['start_date'] = datetime.strptime(
                itinerary['start_date'], '%Y-%m-%d'
            ).replace(tzinfo=pytz.UTC)
        
        if 'end_date' in itinerary:
            itinerary['end_date'] = datetime.strptime(
                itinerary['end_date'], '%Y-%m-%d'
            ).replace(tzinfo=pytz.UTC)
            
        # Convertir fechas de string a objetos datetime para cada región
        for region in itinerary.get('regions', []):
            if 'start_date' in region:
                region['start_date'] = datetime.strptime(
                    region['start_date'], '%Y-%m-%d'
                ).replace(tzinfo=pytz.UTC)
            if 'end_date' in region:
                region['end_date'] = datetime.strptime(
                    region['end_date'], '%Y-%m-%d'
                ).replace(tzinfo=pytz.UTC)
                
        return itinerary
    except Exception as e:
        print(f"Error al cargar el itinerario: {e}")
        # Devolver un itinerario por defecto o vacío en caso de error
        return {
            'title': 'Itinerario no disponible',
            'regions': [],
            'start_date': datetime.now(pytz.UTC),
            'end_date': datetime.now(pytz.UTC)
        }

def get_current_region(itinerary, current_date):
    """
    Determina la región actual basada en la fecha
    
    Args:
        itinerary: Datos del itinerario
        current_date: Fecha actual
        
    Returns:
        dict: Región actual o None si no hay región para la fecha
    """
    for region in itinerary.get('regions', []):
        if (region.get('start_date') <= current_date <= region.get('end_date')):
            return region
    return None

def get_upcoming_regions(itinerary, current_date, limit=3):
    """
    Obtiene las próximas regiones en el itinerario
    
    Args:
        itinerary: Datos del itinerario
        current_date: Fecha actual
        limit: Número máximo de regiones a devolver
        
    Returns:
        list: Lista de próximas regiones
    """
    upcoming = []
    for region in itinerary.get('regions', []):
        if region.get('start_date') > current_date:
            upcoming.append(region)
            if len(upcoming) >= limit:
                break
    return upcoming

def save_itinerary(itinerary, filename):
    """
    Guarda un itinerario en un archivo YAML
    
    Args:
        itinerary: Datos del itinerario
        filename: Nombre del archivo YAML en la carpeta data/itineraries/
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        # Convertir fechas de datetime a string antes de guardar
        itinerary_copy = itinerary.copy()
        for region in itinerary_copy.get('regions', []):
            if 'start_date' in region and isinstance(region['start_date'], datetime):
                region['start_date'] = region['start_date'].strftime('%Y-%m-%d')
            if 'end_date' in region and isinstance(region['end_date'], datetime):
                region['end_date'] = region['end_date'].strftime('%Y-%m-%d')
        
        file_path = os.path.join('data', 'itineraries', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(itinerary_copy, file, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        print(f"Error al guardar el itinerario: {e}")
        return False