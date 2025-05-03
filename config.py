import os

# API Keys
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'c6f2887795fa4271b5d8b06960fc6102')
OPENMETEO_API_URL = "https://api.open-meteo.com/v1/forecast"

# Configuración de itinerarios
DEFAULT_ITINERARY = 'thailand_2025.yaml'

# Configuración de cache
CACHE_TIMEOUT = 1800  # 0.5 hora en segundos

# Configuración de actualización automática
AUTO_UPDATE_INTERVAL = 1800  # 0.5 hora en segundos