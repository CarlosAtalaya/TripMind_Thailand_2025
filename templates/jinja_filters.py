
from datetime import datetime

def now():
    """Función para obtener la fecha y hora actuales para usar en plantillas Jinja2"""
    return datetime.now()