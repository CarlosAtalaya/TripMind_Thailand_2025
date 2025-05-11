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

DANGEROUS_PLANTS = [
    {
        'name': 'Flor de Oleandro',
        'thai_name': 'ยี่โถ (Yi Tho)',
        'image': 'oleander.jpg',
        'description': 'Planta ornamental muy común pero extremadamente tóxica. Todas sus partes son venenosas. Puede causar problemas cardíacos graves si se ingiere.',
        'danger_level': 'Extremo',
        'areas': ['Todo el país', 'Jardines', 'Parques']
    },
    {
        'name': 'Fruto del Manzanillo',
        'thai_name': 'มะขามป้อมพิษ',
        'image': 'manchineel.jpg',
        'description': 'Árbol costero cuyo fruto parece una manzana verde pequeña. Extremadamente tóxico, su savia puede causar quemaduras severas en la piel.',
        'danger_level': 'Extremo',
        'areas': ['Zonas costeras', 'Playas del sur']
    },
    {
        'name': 'Dieffenbachia',
        'thai_name': 'ว่านน้ำเต้า',
        'image': 'dieffenbachia.jpg',
        'description': 'Planta de interior común. Sus hojas contienen cristales de oxalato que pueden causar hinchazón severa de la lengua y garganta si se mastican.',
        'danger_level': 'Alto',
        'areas': ['Hoteles', 'Casas', 'Oficinas']
    },
    {
        'name': 'Ricino',
        'thai_name': 'ละหุ่ง (La Hung)',
        'image': 'castor_bean.jpg',
        'description': 'Sus semillas contienen ricina, una de las sustancias más venenosas conocidas. Masticar las semillas puede ser mortal.',
        'danger_level': 'Extremo',
        'areas': ['Áreas rurales', 'Jardines']
    },
    {
        'name': 'Anturio',
        'thai_name': 'หน้าวัว',
        'image': 'anthurium.jpg',
        'description': 'Popular planta ornamental con flores rojas brillantes. Todas sus partes son tóxicas y pueden causar irritación severa en boca y garganta.',
        'danger_level': 'Moderado',
        'areas': ['Jardines', 'Hoteles', 'Decoración interior']
    },
    {
        'name': 'Lirio de Cala',
        'thai_name': 'ดอกคาล่า',
        'image': 'calla_lily.jpg',
        'description': 'Elegante flor blanca muy usada en decoración. Contiene oxalatos de calcio que causan ardor intenso y problemas para tragar.',
        'danger_level': 'Moderado',
        'areas': ['Hoteles', 'Bodas', 'Eventos']
    }
]

THAI_TRADITIONS = [
    {
        'name': 'Wai (Saludo tradicional)',
        'thai_name': 'ไหว้',
        'image': 'wai_greeting.jpg',
        'description': 'El saludo tradicional tailandés. Se juntan las palmas en posición de oración y se inclina ligeramente. Cuanto más alto las manos y más profunda la inclinación, mayor respeto.',
        'importance': 'Esencial',
        'areas': ['Todo el país'],
        'etiquette': 'Los jóvenes saludan primero a los mayores. No uses el wai con niños o personal de servicio.'
    },
    {
        'name': 'Songkran',
        'thai_name': 'สงกรานต์',
        'image': 'songkran.jpg',
        'description': 'El año nuevo tailandés (13-15 abril). Festival del agua donde la gente se rocía agua como bendición. Es la mayor celebración del país.',
        'importance': 'Alta',
        'areas': ['Todo el país'],
        'etiquette': 'Protege tus dispositivos electrónicos. Viste ropa que se pueda mojar. Respeta a los monjes y ancianos.'
    },
    {
        'name': 'Loy Krathong',
        'thai_name': 'ลอยกระทง',
        'image': 'loy_krathong.jpg',
        'description': 'Festival de las luces flotantes. Se lanzan pequeñas balsas decoradas con velas al agua para pedir perdón a la diosa del agua.',
        'importance': 'Alta',
        'areas': ['Todo el país', 'Especialmente Chiang Mai'],
        'etiquette': 'Usa materiales biodegradables. Pide un deseo mientras sueltas tu krathong. No recuperes krathongs ajenos.'
    },
    {
        'name': 'Respeto a Buda y Monjes',
        'thai_name': 'การเคารพพระ',
        'image': 'monks_respect.jpg',
        'description': 'Los monjes son muy respetados. Las mujeres no deben tocarlos ni entregarles cosas directamente. Todos deben mostrar respeto en templos.',
        'importance': 'Esencial',
        'areas': ['Todo el país', 'Templos'],
        'etiquette': 'Viste modestamente en templos. Quítate los zapatos. No apuntes los pies hacia imágenes de Buda.'
    },
    {
        'name': 'Cabeza y Pies',
        'thai_name': 'ศีรษะและเท้า',
        'image': 'head_feet.jpg',
        'description': 'La cabeza es sagrada, los pies son impuros. Nunca toques la cabeza de alguien ni uses los pies para señalar.',
        'importance': 'Esencial',
        'areas': ['Todo el país'],
        'etiquette': 'No toques la cabeza de nadie, ni de niños. No pongas los pies sobre mesas. No señales con los pies.'
    },
    {
        'name': 'La Monarquía',
        'thai_name': 'สถาบันพระมหากษัตริย์',
        'image': 'monarchy.jpg',
        'description': 'La familia real es profundamente respetada. Cualquier falta de respeto es ilegal y severamente castigada.',
        'importance': 'Crítica',
        'areas': ['Todo el país'],
        'etiquette': 'Levántate cuando suene el himno real. Nunca critiques a la monarquía. Respeta imágenes y billetes con la imagen del rey.'
    }
]

DANGEROUS_PLACES = [
    {
        'name': 'Patpong Night Market',
        'type': 'Barrio Rojo',
        'description': 'Zona de entretenimiento nocturno conocida por sus bares go-go, shows ping pong y negocios de dudosa reputación. Alto riesgo de estafas y sobreprecios.',
        'danger_level': 'Alto',
        'location_url': 'https://maps.google.com/?q=13.7300,100.5339',
        'areas': ['Bangkok'],
        'tips': 'Evita beber bebidas que no hayas visto servir. Pregunta precios antes de consumir. No aceptes invitaciones de desconocidos.'
    },
    {
        'name': 'Soi Cowboy',
        'type': 'Barrio Rojo',
        'description': 'Calle conocida por sus bares go-go y prostitución. Frecuentes estafas con cuentas infladas y drogas en bebidas.',
        'danger_level': 'Alto',
        'location_url': 'https://maps.google.com/?q=13.7378,100.5607',
        'areas': ['Bangkok'],
        'tips': 'No dejes tu bebida sin supervisión. Negocia precios antes. Ten cuidado con las lady drinks infladas.'
    },
    {
        'name': 'Khaosan Road de madrugada',
        'type': 'Zona de fiesta',
        'description': 'Después de las 2 AM, aumentan los robos, peleas y problemas con drogas. La policía hace redadas frecuentes.',
        'danger_level': 'Moderado',
        'location_url': 'https://maps.google.com/?q=13.7586,100.4971',
        'areas': ['Bangkok'],
        'tips': 'Mejor volver al hotel antes de las 2 AM. No compres drogas. Ten cuidado con tus pertenencias.'
    },
    {
        'name': 'Nana Plaza',
        'type': 'Barrio Rojo',
        'description': 'Complejo de entretenimiento adulto con tres pisos de go-go bars. Alto riesgo de estafas y drogas.',
        'danger_level': 'Alto',
        'location_url': 'https://maps.google.com/?q=13.7410,100.5556',
        'areas': ['Bangkok'],
        'tips': 'Evita ir solo. No aceptes bebidas de desconocidos. Cuidado con las cuentas infladas.'
    },
    {
        'name': 'Walking Street Pattaya',
        'type': 'Barrio Rojo',
        'description': 'La calle de entretenimiento nocturno más grande de Tailandia. Prostitución, drogas y estafas abundan.',
        'danger_level': 'Extremo',
        'location_url': 'https://maps.google.com/?q=12.9273,100.8736',
        'areas': ['Pattaya'],
        'tips': 'Extrema precaución. No lleves objetos de valor. Evita conflictos. La policía es corrupta en la zona.'
    },
    {
        'name': 'Zonas fronterizas con Myanmar',
        'type': 'Frontera conflictiva',
        'description': 'Áreas con conflictos armados, tráfico de drogas y personas. Extremadamente peligroso.',
        'danger_level': 'Extremo',
        'location_url': 'https://maps.google.com/?q=19.8316,99.8325',
        'areas': ['Mae Hong Son', 'Tak', 'Kanchanaburi'],
        'tips': 'NO visitar sin guía local autorizado. Evitar completamente de noche. Posibles minas terrestres.'
    },
    {
        'name': 'Mercados nocturnos ilegales',
        'type': 'Mercado negro',
        'description': 'Mercados donde se venden drogas, armas y productos falsificados. Frecuentes redadas policiales.',
        'danger_level': 'Alto',
        'location_url': 'https://maps.google.com/?q=13.7445,100.5100',
        'areas': ['Bangkok', 'Chiang Mai'],
        'tips': 'Evitar completamente. Si te pillan comprando productos ilegales, puedes ir a prisión.'
    },
    {
        'name': 'Khlong Toei Slum',
        'type': 'Barrio marginal',
        'description': 'El barrio de chabolas más grande de Bangkok. Alta criminalidad, drogas y violencia.',
        'danger_level': 'Extremo',
        'location_url': 'https://maps.google.com/?q=13.7196,100.5570',
        'areas': ['Bangkok'],
        'tips': 'NO entrar sin acompañamiento local. Evitar completamente de noche. No sacar cámaras.'
    },
    {
        'name': 'Playas solitarias de Koh Phangan',
        'type': 'Playa peligrosa',
        'description': 'Playas remotas con historial de asaltos y violaciones a turistas. Sin vigilancia ni iluminación.',
        'danger_level': 'Alto',
        'location_url': 'https://maps.google.com/?q=9.7500,100.0500',
        'areas': ['Koh Phangan'],
        'tips': 'Nunca ir solo, especialmente de noche. Informar a alguien de tu ubicación. Llevar spray pimienta.'
    },
    {
        'name': 'Callejones de Chinatown de noche',
        'type': 'Zona peligrosa',
        'description': 'Callejones oscuros con actividad de pandillas, drogas y prostitución ilegal.',
        'danger_level': 'Moderado',
        'location_url': 'https://maps.google.com/?q=13.7390,100.5110',
        'areas': ['Bangkok'],
        'tips': 'Evitar callejones secundarios de noche. Ir en grupo. No mostrar objetos de valor.'
    },
    {
        'name': 'Puentes fronterizos con Camboya',
        'type': 'Frontera',
        'description': 'Zonas de frontera con estafas de visado, robos y corrupción policial.',
        'danger_level': 'Moderado',
        'location_url': 'https://maps.google.com/?q=13.4394,102.8357',
        'areas': ['Sa Kaeo', 'Trat'],
        'tips': 'Usar solo cruces fronterizos oficiales. No confiar en "ayudantes". Tener documentos en regla.'
    },
    {
        'name': 'Soi 6 Pattaya',
        'type': 'Barrio Rojo',
        'description': 'Calle conocida por bares de corta estancia y prostitución. Alta incidencia de robos y drogas.',
        'danger_level': 'Alto',
        'location_url': 'https://maps.google.com/?q=12.9365,100.8843',
        'areas': ['Pattaya'],
        'tips': 'Extrema precaución. No llevar mucho dinero. Evitar conflictos.'
    }
]

# Resumen por regiones basado en tu itinerario
REGIONAL_SUMMARY = {
    'Bangkok': {
        'dangerous_animals': ['Escorpión Negro', 'Araña de Saco Amarillo', 'Ciempiés Gigante'],
        'dangerous_plants': ['Dieffenbachia', 'Anturio', 'Lirio de Cala', 'Flor de Oleandro'],
        'food_specialties': ['Pad Thai', 'Tom Yum Goong', 'Massaman Curry', 'Mango Sticky Rice'],
        'cultural_traditions': ['Wai', 'Respeto a Buda y Monjes', 'Cabeza y Pies', 'La Monarquía'],
        'dangerous_places': ['Patpong Night Market', 'Soi Cowboy', 'Khaosan Road de madrugada', 'Nana Plaza', 'Khlong Toei Slum', 'Callejones de Chinatown de noche']
    },
    'Chiang Mai': {
        'dangerous_animals': ['Cobra Rey', 'Escorpión Negro', 'Mono Macaco', 'Ciempiés Gigante'],
        'dangerous_plants': ['Ricino', 'Flor de Oleandro', 'Dieffenbachia'],
        'food_specialties': ['Khao Soi', 'Sai Oua (salchicha norteña)', 'Nam Prik Ong'],
        'cultural_traditions': ['Loy Krathong', 'Wai', 'Respeto a Buda y Monjes', 'Songkran'],
        'dangerous_places': ['Mercados nocturnos ilegales']
    },
    'Khao Sok': {
        'dangerous_animals': ['Cobra Rey', 'Escorpión Negro', 'Ciempiés Gigante', 'Araña de Saco Amarillo'],
        'dangerous_plants': ['Ricino', 'Flor de Oleandro'],
        'food_specialties': ['Pescados de río', 'Curry selvático', 'Vegetales locales'],
        'cultural_traditions': ['Wai', 'Respeto a Buda y Monjes'],
        'dangerous_places': []
    },
    'Krabi': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Mono Macaco', 'Ciempiés Gigante'],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro', 'Anturio'],
        'food_specialties': ['Mariscos frescos', 'Tom Yum Goong', 'Pescado a la parrilla'],
        'cultural_traditions': ['Wai', 'Respeto a Buda y Monjes', 'Songkran'],
        'dangerous_places': []
    },
    'Phuket': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Ciempiés Gigante'],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro', 'Lirio de Cala'],
        'food_specialties': ['Mariscos', 'Hokkien Mee', 'Oh Tao (tortilla de ostras)'],
        'cultural_traditions': ['Wai', 'Songkran', 'La Monarquía'],
        'dangerous_places': []
    },
    'Koh Phangan': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Ciempiés Gigante'],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro'],
        'food_specialties': ['Pescado fresco', 'Curries de mariscos', 'Frutas tropicales'],
        'cultural_traditions': ['Full Moon Party', 'Wai', 'Respeto a Buda y Monjes'],
        'dangerous_places': ['Playas solitarias de Koh Phangan']
    },
    'Koh Samui': {
        'dangerous_animals': ['Medusa Caja', 'Escorpión Negro', 'Ciempiés Gigante', 'Mono Macaco'],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro', 'Dieffenbachia'],
        'food_specialties': ['Mariscos', 'Som Tam', 'Coconut ice cream'],
        'cultural_traditions': ['Wai', 'Songkran', 'Respeto a Buda y Monjes'],
        'dangerous_places': []
    }
}