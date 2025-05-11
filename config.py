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

# IMPORTANTE: La carpeta multimedia SIEMPRE estará en la raíz del proyecto
# Obtener la ruta absoluta del archivo config.py
CONFIG_FILE_PATH = os.path.abspath(__file__)

# Obtener el directorio donde está config.py (que debería ser la raíz del proyecto)
PROJECT_ROOT = os.path.dirname(CONFIG_FILE_PATH)

# La carpeta multimedia SIEMPRE estará en PROJECT_ROOT/MULTIMEDIA_FOLDER_NAME
MULTIMEDIA_BASE_PATH = os.path.join(PROJECT_ROOT, MULTIMEDIA_FOLDER_NAME)

# Verificación para asegurar que la ruta es correcta
print(f"Raíz del proyecto: {PROJECT_ROOT}")
print(f"Carpeta multimedia configurada en: {MULTIMEDIA_BASE_PATH}")

# Crear la carpeta si no existe
if not os.path.exists(MULTIMEDIA_BASE_PATH):
    try:
        os.makedirs(MULTIMEDIA_BASE_PATH)
        print(f"Carpeta multimedia creada en: {MULTIMEDIA_BASE_PATH}")
    except Exception as e:
        print(f"ERROR: No se pudo crear la carpeta multimedia: {e}")

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
DAILY_PHOTOS_MAX_SIZE = 25 * 1024 * 1024  # 25 MB
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

# Configuracion para guías
DANGEROUS_ANIMALS = [
    {
        'name': 'Cobra Rey',
        'thai_name': 'งูจงอาง (Ngu Chong Ang)',
        'image': 'cobra.jpg',
        'description': 'Una de las serpientes más venenosas de Tailandia. Puede alcanzar hasta 6 metros de longitud. Si la ves, mantén distancia y no la provoques.',
        'danger_level': 'Extremo',
        'areas': ['Kanchanaburi', 'Khao Yai', 'Areas rurales']
    },
    {
        'name': 'Escorpión Negro',
        'thai_name': 'แมงป่อง (Maeng Pong)',
        'image': 'scorpion.jpg',
        'description': 'Común en áreas rocosas y bajo troncos. Su picadura es dolorosa pero raramente mortal. Sacude zapatos antes de ponértelos.',
        'danger_level': 'Moderado',
        'areas': ['Todo el país', 'Especialmente en zonas rurales']
    },
    {
        'name': 'Medusa Caja',
        'thai_name': 'แมงกะพรุนกล่อง (Maeng Kaprun Klong)',
        'image': 'jellyfish.jpg',
        'description': 'Extremadamente venenosa, habita en aguas costeras. Su picadura puede ser mortal. Evitar nadar en temporada de medusas.',
        'danger_level': 'Extremo',
        'areas': ['Phuket', 'Krabi', 'Koh Samui', 'Koh Phangan']
    },
    {
        'name': 'Ciempiés Gigante',
        'thai_name': 'ตะขาบ (Takhap)',
        'image': 'centipede.jpg',
        'description': 'Puede crecer hasta 20 cm. Su mordedura es muy dolorosa y puede causar infección. Se esconde en lugares húmedos.',
        'danger_level': 'Alto',
        'areas': ['Todo el país', 'Especialmente en zonas húmedas']
    },
    {
        'name': 'Mono Macaco',
        'thai_name': 'ลิง (Ling)',
        'image': 'macaque.jpg',
        'description': 'Aunque parezcan amigables, pueden morder y transmitir rabia. No alimentes ni toques a los monos.',
        'danger_level': 'Moderado',
        'areas': ['Lopburi', 'Templos', 'Parques nacionales']
    },
    {
        'name': 'Araña de Saco Amarillo',
        'thai_name': 'แมงมุมถุงเหลือง',
        'image': 'spider.jpg',
        'description': 'Pequeña pero venenosa. Su mordedura causa dolor e hinchazón. Común en casas y hoteles.',
        'danger_level': 'Bajo-Moderado',
        'areas': ['Áreas urbanas', 'Hoteles', 'Casas']
    }
]

THAI_FOOD = [
    {
        'name': 'Pad Thai',
        'thai_name': 'ผัดไทย',
        'image': 'pad_thai.jpg',
        'description': 'Fideos de arroz salteados con huevo, tofu, gambas o pollo, cacahuetes y brotes de soja. El plato nacional de Tailandia.',
        'spicy_level': 'Suave',
        'areas': ['Todo el país'],
        'price_range': '40-80 THB'
    },
    {
        'name': 'Tom Yum Goong',
        'thai_name': 'ต้มยำกุ้ง',
        'image': 'tom_yum.jpg',
        'description': 'Sopa picante y ácida con gambas, setas, limoncillo, hojas de lima kaffir y chiles. Plato emblemático tailandés.',
        'spicy_level': 'Muy picante',
        'areas': ['Todo el país'],
        'price_range': '80-150 THB'
    },
    {
        'name': 'Som Tam',
        'thai_name': 'ส้มตำ',
        'image': 'som_tam.jpg',
        'description': 'Ensalada de papaya verde con tomates, judías largas, cacahuetes, gambas secas y chiles. Refrescante pero picante.',
        'spicy_level': 'Picante',
        'areas': ['Isaan', 'Bangkok'],
        'price_range': '30-60 THB'
    },
    {
        'name': 'Khao Soi',
        'thai_name': 'ข้าวซอย',
        'image': 'khao_soi.jpg',
        'description': 'Curry de coco con fideos de huevo, pollo o ternera, típico del norte. Servido con fideos crujientes encima.',
        'spicy_level': 'Moderado',
        'areas': ['Chiang Mai', 'Norte de Tailandia'],
        'price_range': '50-100 THB'
    },
    {
        'name': 'Mango Sticky Rice',
        'thai_name': 'ข้าวเหนียวมะม่วง',
        'image': 'mango_sticky_rice.jpg',
        'description': 'Postre de arroz glutinoso con leche de coco servido con mango maduro. Perfecto para el clima tropical.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '50-100 THB'
    },
    {
        'name': 'Massaman Curry',
        'thai_name': 'แกงมัสมั่น',
        'image': 'massaman.jpg',
        'description': 'Curry suave con influencia india, con carne, patatas, cacahuetes y especias aromáticas.',
        'spicy_level': 'Suave',
        'areas': ['Sur de Tailandia', 'Bangkok'],
        'price_range': '60-120 THB'
    }
]

# Resumen por regiones basado en tu itinerario
REGIONAL_SUMMARY = {
    'Bangkok': {
        'dangerous_animals': ['Escorpión Negro', 'Araña de Saco Amarillo', 'Ciempiés Gigante'],
        'food_specialties': ['Pad Thai', 'Tom Yum Goong', 'Massaman Curry', 'Mango Sticky Rice']
    },
    'Chiang Mai': {
        'dangerous_animals': ['Cobra Rey', 'Escorpión Negro', 'Mono Macaco', 'Ciempiés Gigante'],
        'food_specialties': ['Khao Soi', 'Sai Oua (salchicha norteña)', 'Nam Prik Ong']
    },
    'Khao Sok': {
        'dangerous_animals': ['Cobra Rey', 'Escorpión Negro', 'Ciempiés Gigante', 'Araña de Saco Amarillo'],
        'food_specialties': ['Pescados de río', 'Curry selvático', 'Vegetales locales']
    },
    'Krabi': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Mono Macaco', 'Ciempiés Gigante'],
        'food_specialties': ['Mariscos frescos', 'Tom Yum Goong', 'Pescado a la parrilla']
    },
    'Phuket': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Ciempiés Gigante'],
        'food_specialties': ['Mariscos', 'Hokkien Mee', 'Oh Tao (tortilla de ostras)']
    },
    'Koh Phangan': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Ciempiés Gigante'],
        'food_specialties': ['Pescado fresco', 'Curries de mariscos', 'Frutas tropicales']
    },
    'Koh Samui': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Ciempiés Gigante', 'Mono Macaco'],
        'food_specialties': ['Mariscos', 'Som Tam', 'Coconut ice cream']
    }
}