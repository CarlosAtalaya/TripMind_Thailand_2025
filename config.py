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

# Configuración de archivos multimedia
MULTIMEDIA_FOLDER_NAME = 'Multimedia_Tailandia2025'

# Permitir configuración personalizada mediante variable de entorno
CUSTOM_MULTIMEDIA_PATH = os.environ.get('MULTIMEDIA_PATH')

if CUSTOM_MULTIMEDIA_PATH:
    MULTIMEDIA_BASE_PATH = CUSTOM_MULTIMEDIA_PATH
else:
    # Ruta relativa desde la ubicación del proyecto (un nivel arriba)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MULTIMEDIA_BASE_PATH = os.path.join(os.path.dirname(PROJECT_ROOT), MULTIMEDIA_FOLDER_NAME)

# Límites de almacenamiento
MAX_UPLOAD_SIZE = 6 * 1024 * 1024 * 1024  # 6 GB en bytes
MAX_FOLDER_SIZE = 400 * 1024 * 1024 * 1024  # 400 GB en bytes

ALLOWED_EXTENSIONS = {
    # Imágenes
    'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'tif', 'svg', 'heic', 'heif',
    # Videos
    'mp4', 'mov', 'avi', 'wmv', 'flv', 'mkv', 'webm', 'm4v', 'mpg', 'mpeg', '3gp',
    # Audio
    'mp3', 'wav', 'aac', 'flac', 'm4a', 'wma', 'ogg',
    # Documentos
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf', 'odt', 'ods', 'odp',
    # Archivos comprimidos
    'zip', 'rar', '7z', 'tar', 'gz', 'bz2',
    # Otros formatos útiles
    'json', 'xml', 'csv', 'md', 'html', 'htm', 'css', 'js',
    # Formatos de imagen raw/profesionales
    'raw', 'cr2', 'nef', 'arw', 'dng'
}