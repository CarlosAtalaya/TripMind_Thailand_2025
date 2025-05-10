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
    # La carpeta multimedia estará en la raíz del proyecto
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MULTIMEDIA_BASE_PATH = os.path.join(PROJECT_ROOT, MULTIMEDIA_FOLDER_NAME)

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

# Configuración de fotos diarias (daily_photos.py)
DAILY_PHOTOS_FOLDER = 'Dailys_photos'
DAILY_PHOTOS_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
DAILY_PHOTOS_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
DAILY_DEADLINE_HOUR = 20  # 8 PM hora tailandesa
THAILAND_TZ = 'Asia/Bangkok'

# Configuración de votaciones (votes.py)
VOTE_CATEGORIES = [
    {"name": "MVP diario", "description": "El más valioso del día"},
    {"name": "Donde está Wally", "description": "El que más se pierde"},
    {"name": "Foto del día", "description": "La mejor foto"},
    {"name": "Fue con fé, no con lógica", "description": "Decisiones cuestionables"},
    {"name": "Mamá ven a por mí", "description": "El más desvalido"},
    {"name": "Fashion Victim, Luis Butrón", "description": "El mejor/peor vestido"},
    {"name": "Pa el Tinder", "description": "La foto más seductora"},
    {"name": "El seguro no cubre esto", "description": "La situación más arriesgada"}
]

# Configuración de noticias (news.py)
NEWS_ALERT_KEYWORDS = [
    # Seguridad y emergencias
    'alert', 'security', 'protest', 'emergency', 'evacuation', 'earthquake',
    'storm', 'rain', 'flood', 'travel warning', 'demonstration', 'danger',
    'violence', 'outbreak', 'covid', 'hurricane', 'tsunami', 'closure', 'strike',
    'terrorist', 'attack', 'police', 'military', 'curfew', 'lockdown',
    'accident', 'crash', 'fire', 'explosion', 'incident', 'crisis',
    
    # Salud y enfermedades
    'disease', 'virus', 'infection', 'outbreak', 'hospital', 'medical', 'health',
    'dengue', 'malaria', 'fever', 'vaccination', 'quarantine', 'pandemic',
    
    # Transporte y turismo
    'tourist', 'tourism', 'airport', 'flight', 'canceled', 'delayed', 'transport',
    'road closure', 'traffic', 'visa', 'immigration', 'embassy', 'consulate',
    'backpacker', 'hotel', 'hostel', 'ferry', 'train', 'bus',
    
    # Clima y desastres naturales
    'weather', 'monsoon', 'typhoon', 'landslide', 'drought', 'heatwave',
    'temperature', 'humidity', 'forecast', 'season', 'tropical storm',
    
    # Cultura y entretenimiento (incluyendo términos graciosos)
    'ladyboy', 'kathoey', 'nightlife', 'red light', 'ping pong show', 'full moon party',
    'massage parlor', 'happy ending', 'tuk tuk', 'scam', 'tourist trap',
    'bar girl', 'go go bar', 'soapy massage', 'karaoke', 'walking street',
    
    # Términos específicos de viajeros españoles
    'spanish tourist', 'spanish group', 'español', 'españoles', 'turista español',
    'group tour', 'party', 'fiesta', 'alcohol', 'drunk', 'arrest', 'jail',
    
    # Otros términos relevantes
    'drugs', 'marijuana', 'cannabis', 'mushrooms', 'police raid', 'fine', 'penalty',
    'money', 'atm', 'credit card', 'theft', 'robbery', 'pickpocket',
    'food poisoning', 'stomach', 'diarrhea', 'doctor', 'clinic',
    'temple', 'buddha', 'monk', 'festival', 'celebration', 'holiday',
    'beach', 'island', 'diving', 'snorkeling', 'boat', 'speedboat'
]

NEWS_RSS_FEEDS = [
    'https://www.bangkokpost.com/rss/data/topstories.xml',
    'https://thethaiger.com/feed',
    'https://news.google.com/rss/search?q=thailand&hl=en-US&gl=US&ceid=US:en',
    'https://www.channelnewsasia.com/api/v1/rss-outbound-feed/latest_news'
]