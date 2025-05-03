"""
TravelBoard - Filtros Personalizados para Jinja2

Define filtros personalizados que se pueden usar en las plantillas Jinja2.
"""
from datetime import datetime

def format_date(date_string):
    """
    Formatea una cadena de fecha para mostrarla de forma legible
    
    Args:
        date_string: Fecha en formato ISO o datetime
        
    Returns:
        str: Fecha formateada
    """
    if not date_string:
        return ''
    
    try:
        # Si es un string, convertirlo a datetime
        if isinstance(date_string, str):
            # Manejar diferentes formatos posibles
            if 'T' in date_string:
                # Formato ISO completo con hora
                date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                # Formato solo fecha
                date = datetime.strptime(date_string, '%Y-%m-%d')
        else:
            # Asumir que ya es un objeto datetime
            date = date_string
            
        # Calcular la diferencia con la fecha actual
        now = datetime.now()
        diff_days = (now.date() - date.date()).days
        
        # Formatos según la diferencia de días
        if diff_days == 0:
            return f"Hoy, {date.strftime('%H:%M')}"
        elif diff_days == 1:
            return f"Ayer, {date.strftime('%H:%M')}"
        elif diff_days > 1 and diff_days < 7:
            return date.strftime('%A, %d %b')  # Ejemplo: "Lunes, 15 Jul"
        elif date.year == now.year:
            return date.strftime('%d %b')  # Ejemplo: "15 Jul"
        else:
            return date.strftime('%d %b %Y')  # Ejemplo: "15 Jul 2025"
    except Exception as e:
        print(f"Error al formatear fecha: {e}")
        return date_string  # Devolver la entrada original si hay error