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
DAILY_PHOTOS_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'tif', 'svg', 'heic', 'heif'}
DAILY_PHOTOS_MAX_SIZE = 50 * 1024 * 1024  # 50 MB

DAILY_DEADLINE_HOUR = 22  # 10 PM hora tailandesa
VOTING_DEADLINE_HOUR = 20  # 10 PM hora tailandesa

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

# Elementos del checklist organizados por categorías
CHECKLIST_ITEMS = {
    'documentos': {
        'name': 'Documentación',
        'icon': 'fas fa-passport',
        'color': 'danger',
        'items': {
            'pasaporte': 'Pasaporte (válido mín. 6 meses)',
            'identificador': 'DNI',
            'carnet_internacional': 'Carnet conducir internacional',
            'seguro_viaje': 'Seguro de viaje',
            'tarjetas': 'Tarjetas de crédito/débito',
            'efectivo': 'Efectivo (euros para cambiar)',
            'fotocopias': 'Fotocopias de documentos (puretas)',
            'tarjeta_embarque': 'Tarjetas de embarque (móvil)',
            'reservas_hoteles': 'Confirmaciones de hoteles',
            'itinerario': 'Itinerario impreso (pagina web de 1 mes de trabajo en su defecto)'
        }
    },
    'ropa': {
        'name': 'Ropa y Calzado',
        'icon': 'fas fa-tshirt',
        'color': 'primary',
        'items': {
            'camisetas_ligeras': 'Camisetas de manga corta (5-7)',
            'pantalones_cortos': 'Pantalones cortos (3-4)',
            'pantalones_largos': 'Pantalones largos (2-3) - templos',
            'vestidos': 'Vestidos/faldas largas - templos',
            'ropa_interior': 'Ropa interior (7-10 mudas)',
            'calcetines': 'Calcetines (7-10 pares)',
            'ropa_interior': 'Calzones/Bragas/Tangas mercadillo (8)',
            'pijama': 'Pijama/ropa de dormir',
            'chanclas': 'Chanclas para la ducha',
            'zapatillas_comodas': 'Zapatillas cómodas para caminar',
            'sandalias': 'Sandalias',
            'ropa_lluvia': 'Chubasquero/poncho',
            'bañador': 'Bañador/bikini (2)',
            'gorra': 'Gorra/sombrero'
        }
    },
    'higiene': {
        'name': 'Higiene y Cuidado',
        'icon': 'fas fa-pump-soap',
        'color': 'info',
        'items': {
            'cepillo_dientes': 'Cepillo de dientes',
            'pasta_dientes': 'Pasta de dientes',
            'champu': 'Champú',
            'desodorante': 'Desodorante',
            'protector_solar': 'Protector solar (SPF 50+)',
            'after_sun': 'After sun/aloe vera',
            'repelente': 'Repelente de mosquitos (DEET)',
            'toallas': 'Toallas de microfibra (1)',
            'productos_femeninos': 'Productos de higiene femenina',
            'afeitado': 'Kit de afeitado (se lo lleva Luis)',
            'perfume': 'Perfume/colonia (se coge de Isisdro)'
        }
    },
    'botiquin': {
        'name': 'Botiquín y Salud',
        'icon': 'fas fa-first-aid',
        'color': 'success',
        'items': {
            'paracetamol': 'Paracetamol/ibuprofeno',
            'antidiarreicos': 'Antidiarreicos (Fortasec)',
            'probioticos': 'Probióticos',
            'antihistaminicos': 'Antihistamínicos (picaduras)',
            'antiseptico': 'Antiséptico/alcohol (por si pica un Ladyboy)',
            'tiritas': 'Tiritas/vendas',
            'termometro': 'Termómetro (rectal)',
            'medicacion_personal': 'Medicación personal',
            'gel_antibacterial': 'Gel antibacterial',
            'rodillera': 'Rodillera (Isi)'
        }
    },
    'tecnologia': {
        'name': 'Tecnología',
        'icon': 'fas fa-mobile-alt',
        'color': 'warning',
        'items': {
            'movil': 'Teléfono móvil',
            'cargador_movil': 'Cargador del móvil',
            'power_bank': 'Power bank/batería externa',
            'cable_usb': 'Cables USB extra',
            'adaptador_corriente': 'Adaptador de corriente universal',
            'camara': 'Cámara de fotos',
            'cargador_camara': 'Cargador de cámara',
            'tarjeta_memoria': 'Tarjetas de memoria extra',
            'auriculares': 'Auriculares',
            'funda_estanca': 'Funda estanca para móvil'
        }
    },
    'viaje': {
        'name': 'Accesorios de Viaje',
        'icon': 'fas fa-suitcase',
        'color': 'secondary',
        'items': {
            'maleta': 'Mochila principal',
            'candados': 'Candados para maletas',
            'riñonera': 'Riñonera/bolso pequeño',
            'mochila_dia': 'Mochila para excursiones',
            'tapones_oidos': 'Tapones antironquidos de Alfon',
            'bolsas_plastico': 'Bolsas de plástico(3)/zip'
        }
    },
    'otros': {
        'name': 'Otros Esenciales',
        'icon': 'fas fa-plus-circle',
        'color': 'dark',
        'items': {
            'agua_botella': 'Botella de agua reutilizable',
            'snacks': 'Snacks para el vuelo',
            'libro_guia': 'Guía de viaje',
            'cuaderno': 'Cuaderno y bolígrafo (invente Román)',
            'gafas_sol': 'Gafas de sol',
            'linterna': 'Linterna pequeña/frontal',
            'navaja_suiza': 'Navaja suiza (ojo no es mala)',
            'papel_higienico': 'Clinex',
            'toallitas_humedas': 'Toallitas húmedas',
            'dinero_emergencia': 'Dinero de emergencia escondido'
        }
    }
}

# Configuracion para guías
# Reptiles peligrosos de Tailandia
DANGEROUS_REPTILES = [
    {
        'name': 'Cobra Rey',
        'thai_name': 'งูจงอาง (Ngu Chong Ang)',
        'image': 'cobra_rey.jpg',
        'description': 'La serpiente venenosa más larga del mundo. Puede alcanzar hasta 6 metros de longitud. Su veneno es altamente neurotóxico y puede ser mortal en 30 minutos.',
        'danger_level': 'Extremo',
        'areas': ['Kanchanaburi', 'Khao Yai', 'Áreas rurales', 'Parques nacionales'],
        'habitat': 'Selvas, bambuzales, cerca de agua',
        'behavior': 'Agresiva cuando protege su nido, se yergue hasta 1/3 de su longitud'
    },
    {
        'name': 'Cobra Siamés',
        'thai_name': 'งูเห่า (Ngu Hao)',
        'image': 'cobra_siames.jpg',
        'description': 'Cobra altamente venenosa con capucha distintiva. Puede escupir veneno hasta 3 metros de distancia, causando ceguera temporal.',
        'danger_level': 'Extremo',
        'areas': ['Bangkok', 'Chiang Mai', 'Áreas urbanas', 'Campos de arroz'],
        'habitat': 'Zonas habitadas, jardines, edificios abandonados',
        'behavior': 'Escupe veneno cuando se siente amenazada, muy territorial'
    },
    {
        'name': 'Víbora de Russell',
        'thai_name': 'งูสามเหลี่ยม (Ngu Sam Liam)',
        'image': 'vibora_russell.jpg',
        'description': 'Una de las serpientes más peligrosas de Asia. Responsable de la mayoría de mordeduras fatales. Su veneno causa hemorragias severas.',
        'danger_level': 'Extremo',
        'areas': ['Todo el país', 'Campos agrícolas', 'Áreas rurales'],
        'habitat': 'Campos abiertos, plantaciones, cerca de asentamientos humanos',
        'behavior': 'Agresiva y territorial, se camufla muy bien'
    },
    {
        'name': 'Krait Rayado',
        'thai_name': 'งูสวาดลาย (Ngu Sawad Lai)',
        'image': 'krait_rayado.jpg',
        'description': 'Serpiente extremadamente venenosa, activa de noche. Su mordedura es casi indolora pero puede causar parálisis respiratoria.',
        'danger_level': 'Extremo',
        'areas': ['Todo el país', 'Especialmente sur de Tailandia'],
        'habitat': 'Casas, debajo de camas, espacios oscuros',
        'behavior': 'Nocturna, busca refugio en casas durante el día'
    },
    {
        'name': 'Pitón Reticulada',
        'thai_name': 'งูเหลือม (Ngu Lhuam)',
        'image': 'piton_reticulada.jpg',
        'description': 'Una de las serpientes más largas del mundo, puede superar los 8 metros. No venenosa pero mata por constricción.',
        'danger_level': 'Alto',
        'areas': ['Parques nacionales', 'Selvas', 'Cerca de agua'],
        'habitat': 'Árboles, cerca de ríos y lagos',
        'behavior': 'Embosca a sus presas, excelente nadadora'
    },
    {
        'name': 'Cocodrilo de Agua Salada',
        'thai_name': 'จระเข้น้ำเค็ม (Jorakhe Nam Khem)',
        'image': 'cocodrilo_agua_salada.jpg',
        'description': 'El reptil más grande y peligroso de Tailandia. Puede crecer hasta 7 metros. Extremadamente agresivo y territorial.',
        'danger_level': 'Extremo',
        'areas': ['Krabi', 'Phuket', 'Manglares del sur'],
        'habitat': 'Estuarios, manglares, ríos costeros',
        'behavior': 'Emboscadas desde el agua, death roll mortal'
    },
    {
        'name': 'Cocodrilo Siamés',
        'thai_name': 'จระเข้น้ำจืด (Jorakhe Nam Jued)',
        'image': 'cocodrilo_siames.jpg',
        'description': 'Cocodrilo de agua dulce en peligro de extinción. Menos agresivo que su primo de agua salada pero igualmente peligroso.',
        'danger_level': 'Alto',
        'areas': ['Parques nacionales', 'Ríos del interior'],
        'habitat': 'Ríos, lagos, pantanos de agua dulce',
        'behavior': 'Más tímido, pero protege agresivamente su territorio'
    },
    {
        'name': 'Gecko Tokay',
        'thai_name': 'ตุ๊กแก (Tuk Gae)',
        'image': 'gecko_tokay.jpg',
        'description': 'Lagarto grande con mordedura muy fuerte. No venenoso pero su mordida puede infectarse fácilmente. Muy territorial.',
        'danger_level': 'Moderado',
        'areas': ['Todo el país', 'Casas', 'Hoteles'],
        'habitat': 'Techos, paredes, espacios urbanos',
        'behavior': 'Nocturno, territorial, mordedura muy dolorosa'
    }
]

# Insectos y arácnidos peligrosos de Tailandia
DANGEROUS_INSECTS = [
    {
        'name': 'Escorpión Negro Asiático',
        'thai_name': 'แมงป่องดำ (Maeng Pong Dam)',
        'image': 'escorpion_negro.jpg',
        'description': 'Escorpión altamente venenoso. Su picadura causa dolor extremo, convulsiones y puede ser mortal para niños y ancianos.',
        'danger_level': 'Alto',
        'areas': ['Todo el país', 'Zonas rocosas', 'Bosques'],
        'habitat': 'Debajo de piedras, troncos, zapatos',
        'behavior': 'Nocturno, se esconde durante el día'
    },
    {
        'name': 'Ciempiés Gigante',
        'thai_name': 'ตะขาบยักษ์ (Takhap Yak)',
        'image': 'ciempies_gigante.jpg',
        'description': 'Puede crecer hasta 30 cm. Su mordedura inyecta veneno que causa dolor severo, hinchazón y necrosis local.',
        'danger_level': 'Alto',
        'areas': ['Todo el país', 'Zonas húmedas'],
        'habitat': 'Debajo de troncos, hojarasca, baños húmedos',
        'behavior': 'Nocturno, muy agresivo cuando se ve amenazado'
    },
    {
        'name': 'Araña Viuda Negra',
        'thai_name': 'แมงมุมแม่ม่าย (Maeng Mum Mae Mai)',
        'image': 'viuda_negra.jpg',
        'description': 'Araña altamente venenosa con marca roja distintiva. Su mordedura puede causar latrodectismo, potencialmente mortal.',
        'danger_level': 'Alto',
        'areas': ['Todo el país', 'Espacios oscuros'],
        'habitat': 'Rincones oscuros, cobertizos, baños',
        'behavior': 'Tímida pero agresiva si se ve amenazada'
    },
    {
        'name': 'Araña de Saco Amarillo',
        'thai_name': 'แมงมุมถุงเหลือง (Maeng Mum Tung Lhuang)',
        'image': 'araña_saco_amarillo.jpg',
        'description': 'Pequeña pero venenosa. Su mordedura causa dolor, hinchazón y necrosis. Común en hoteles y casas.',
        'danger_level': 'Moderado',
        'areas': ['Áreas urbanas', 'Hoteles', 'Casas'],
        'habitat': 'Esquinas de techos, cortinas, ropa',
        'behavior': 'Construye sacos de seda, activa de noche'
    },
    {
        'name': 'Avispa Gigante Asiática',
        'thai_name': 'ต่อนรก (Ton Narok)',
        'image': 'avispa_gigante.jpg',
        'description': 'La avispa más grande del mundo. Su picadura es extremadamente dolorosa y puede causar shock anafiláctico.',
        'danger_level': 'Alto',
        'areas': ['Montañas del norte', 'Bosques'],
        'habitat': 'Nidos en árboles, tierra',
        'behavior': 'Extremadamente agresiva, ataca en grupo'
    },
    {
        'name': 'Hormiga Bala',
        'thai_name': 'มดกระสุน (Mot Krasun)',
        'image': 'hormiga_bala.jpg',
        'description': 'Su picadura es considerada una de las más dolorosas del reino animal. El dolor puede durar hasta 24 horas.',
        'danger_level': 'Alto',
        'areas': ['Selvas del sur', 'Parques nacionales'],
        'habitat': 'Árboles, selva tropical',
        'behavior': 'Muy territorial, ataca sin provocación'
    },
    {
        'name': 'Mosquito Dengue',
        'thai_name': 'ยุงลาย (Yung Lai)',
        'image': 'mosquito_dengue.jpg',
        'description': 'Vector del dengue, chikungunya y Zika. Activo durante el día. Las enfermedades que transmite pueden ser mortales.',
        'danger_level': 'Alto',
        'areas': ['Todo el país', 'Especialmente áreas urbanas'],
        'habitat': 'Agua estancada, recipientes',
        'behavior': 'Pica durante el día, especialmente al amanecer y atardecer'
    },
    {
        'name': 'Araña Lobo',
        'thai_name': 'แมงมุมหมาป่า (Maeng Mum Ma Pa)',
        'image': 'araña_lobo.jpg',
        'description': 'Araña cazadora agresiva. Su mordedura causa dolor, hinchazón y puede infectarse. No construye telarañas.',
        'danger_level': 'Moderado',
        'areas': ['Todo el país', 'Jardines', 'Casas'],
        'habitat': 'Suelo, jardines, espacios abiertos',
        'behavior': 'Cazadora activa, salta sobre sus presas'
    }
]

# Mamíferos peligrosos de Tailandia
DANGEROUS_MAMMALS = [
    {
        'name': 'Elefante Asiático',
        'thai_name': 'ช้างเอเชีย (Chang Asia)',
        'image': 'elefante_asiatico.jpg',
        'description': 'Pueden ser impredecibles y extremadamente peligrosos. Los machos en temporada de apareamiento son especialmente agresivos.',
        'danger_level': 'Extremo',
        'areas': ['Chiang Mai', 'Parques nacionales', 'Santuarios'],
        'habitat': 'Selvas, santuarios, campamentos turísticos',
        'behavior': 'Pueden cargar sin aviso, especialmente machos en musth'
    },
    {
        'name': 'Búfalo de Agua',
        'thai_name': 'ควาย (Kwai)',
        'image': 'bufalo_agua.jpg',
        'description': 'Animal muy territorial y agresivo. Sus cuernos pueden atravesar un cuerpo humano. Responsable de muchas muertes anuales.',
        'danger_level': 'Alto',
        'areas': ['Campos de arroz', 'Áreas rurales', 'Todo el país'],
        'habitat': 'Campos inundados, cerca de agua',
        'behavior': 'Extremadamente territorial, carga directamente'
    },
    {
        'name': 'Mono Macaco',
        'thai_name': 'ลิงแสม (Ling Saem)',
        'image': 'macaco_tailandes.jpg',
        'description': 'Pueden morder y transmitir rabia, hepatitis B y herpes B. Muy agresivos cuando protegen comida o crías.',
        'danger_level': 'Moderado',
        'areas': ['Lopburi', 'Templos', 'Parques nacionales'],
        'habitat': 'Templos, áreas urbanas, bosques',
        'behavior': 'Roban comida, muerden si se sienten amenazados'
    },
    {
        'name': 'Jabalí',
        'thai_name': 'หมูป่า (Mu Pa)',
        'image': 'jabali_tailandes.jpg',
        'description': 'Muy agresivos y territoriales. Sus colmillos pueden causar heridas profundas. Cargan en línea recta.',
        'danger_level': 'Alto',
        'areas': ['Parques nacionales', 'Bosques', 'Norte de Tailandia'],
        'habitat': 'Bosques densos, áreas montañosas',
        'behavior': 'Carga directamente cuando se siente amenazado'
    },
    {
        'name': 'Oso Malayo',
        'thai_name': 'หมีควาย (Mi Kwai)',
        'image': 'oso_malayo.jpg',
        'description': 'El oso más pequeño pero muy agresivo. Sus garras pueden causar heridas mortales. Ataca sin provocación.',
        'danger_level': 'Extremo',
        'areas': ['Parques nacionales', 'Selvas del sur'],
        'habitat': 'Selvas densas, áreas montañosas',
        'behavior': 'Impredecible, puede atacar sin aviso'
    },
    {
        'name': 'Perro Callejero',
        'thai_name': 'หมาจรจัด (Ma Jorajat)',
        'image': 'perro_callejero.jpg',
        'description': 'Vector principal de la rabia en Tailandia. Pueden atacar en manadas, especialmente de noche.',
        'danger_level': 'Alto',
        'areas': ['Todo el país', 'Especialmente áreas urbanas'],
        'habitat': 'Calles, mercados, zonas urbanas',
        'behavior': 'Territorial, ataca en grupo, especialmente nocturno'
    },
    {
        'name': 'Murciélago Vampiro',
        'thai_name': 'ค้างคาวแวมไพร์ (Kang Kao Vampire)',
        'image': 'murcielago_vampiro.jpg',
        'description': 'Puede transmitir rabia y otros virus. Su mordedura es casi imperceptible y puede infectar mientras duermes.',
        'danger_level': 'Moderado',
        'areas': ['Cuevas', 'Edificios abandonados', 'Áticos'],
        'habitat': 'Cuevas, techos, espacios oscuros',
        'behavior': 'Nocturno, se alimenta de sangre mientras duermes'
    },
    {
        'name': 'Leopardo Nebuloso',
        'thai_name': 'เสือดาวเมฆ (Suea Dao Megh)',
        'image': 'leopardo_nebuloso.jpg',
        'description': 'Felino salvaje altamente territorial. Excelente trepador, ataca desde los árboles. Muy sigiloso y peligroso.',
        'danger_level': 'Extremo',
        'areas': ['Parques nacionales', 'Selvas remotas'],
        'habitat': 'Copas de árboles, selva densa',
        'behavior': 'Embosca desde árboles, cazador solitario'
    }
]

# Animales acuáticos peligrosos de Tailandia
DANGEROUS_AQUATIC = [
    {
        'name': 'Medusa Caja',
        'thai_name': 'แมงกะพรุนกล่อง (Maeng Kaprun Klong)',
        'image': 'medusa_caja.jpg',
        'description': 'Una de las criaturas más venenosas del mundo. Su picadura puede matar en minutos causando paro cardíaco.',
        'danger_level': 'Extremo',
        'areas': ['Phuket', 'Krabi', 'Koh Samui', 'Koh Phangan', 'Costas del sur'],
        'habitat': 'Aguas costeras tropicales, especialmente en temporada de lluvias',
        'behavior': 'Transparente, casi invisible, tentáculos de hasta 3 metros'
    },
    {
        'name': 'Pez Piedra',
        'thai_name': 'ปลาหิน (Pla Hin)',
        'image': 'pez_piedra.jpg',
        'description': 'El pez más venenoso del mundo. Se camufla perfectamente como una roca. Su espina inyecta veneno mortal.',
        'danger_level': 'Extremo',
        'areas': ['Todas las costas', 'Arrecifes de coral'],
        'habitat': 'Fondos rocosos, arrecifes, aguas poco profundas',
        'behavior': 'Inmóvil, se camufla perfectamente, ataque defensivo'
    },
    {
        'name': 'Serpiente Marina',
        'thai_name': 'งูทะเล (Ngu Talay)',
        'image': 'serpiente_marina.jpg',
        'description': 'Altamente venenosa, su veneno es 10 veces más potente que el de la cobra. Respira aire pero vive en el mar.',
        'danger_level': 'Extremo',
        'areas': ['Golfo de Tailandia', 'Mar de Andamán'],
        'habitat': 'Aguas costeras, arrecifes, estuarios',
        'behavior': 'Generalmente dócil pero mortal si se manipula'
    },
    {
        'name': 'Tiburón Toro',
        'thai_name': 'ฉลามกระทิง (Chalam Krathing)',
        'image': 'tiburon_toro.jpg',
        'description': 'Uno de los tiburones más agresivos. Puede remontar ríos de agua dulce. Responsable de muchos ataques fatales.',
        'danger_level': 'Extremo',
        'areas': ['Costas del sur', 'Estuarios', 'Algunos ríos'],
        'habitat': 'Aguas costeras, estuarios, puede entrar en ríos',
        'behavior': 'Muy territorial y agresivo, ataca sin provocación'
    },
    {
        'name': 'Raya Venenosa',
        'thai_name': 'ปลากระเบนพิษ (Pla Kraben Pit)',
        'image': 'raya_venenosa.jpg',
        'description': 'Su aguijón venenoso puede atravesar el pecho. El veneno causa dolor extremo y puede ser mortal.',
        'danger_level': 'Alto',
        'areas': ['Todas las costas', 'Bahías poco profundas'],
        'habitat': 'Fondos arenosos, aguas poco profundas',
        'behavior': 'Se entierra en arena, ataque defensivo con la cola'
    },
    {
        'name': 'Pulpo de Anillos Azules',
        'thai_name': 'ปลาหมึกวงแหวนน้ำเงิน (Pla Muek Wong Waen Nam Ngern)',
        'image': 'pulpo_anillos_azules.jpg',
        'description': 'Pequeño pero extremadamente venenoso. Su mordedura puede causar parálisis y muerte por asfixia en minutos.',
        'danger_level': 'Extremo',
        'areas': ['Pozas de marea', 'Arrecifes', 'Costas rocosas'],
        'habitat': 'Grietas en rocas, pozas de marea',
        'behavior': 'Muestra anillos azules cuando se ve amenazado'
    },
    {
        'name': 'Pez León',
        'thai_name': 'ปลาสิงโต (Pla Sing To)',
        'image': 'pez_leon.jpg',
        'description': 'Sus espinas contienen veneno que causa dolor extremo, náuseas y puede causar problemas cardíacos.',
        'danger_level': 'Alto',
        'areas': ['Arrecifes de coral', 'Aguas tropicales'],
        'habitat': 'Arrecifes, grietas en rocas',
        'behavior': 'Territorial, despliega aletas cuando se siente amenazado'
    },
    {
        'name': 'Medusa Irukandji',
        'thai_name': 'แมงกะพรุนอิรุกันดจิ (Maeng Kaprun Irukandji)',
        'image': 'medusa_irukandji.jpg',
        'description': 'Diminuta pero letal. Su picadura causa el síndrome de Irukandji: dolor extremo, hipertensión y muerte.',
        'danger_level': 'Extremo',
        'areas': ['Aguas tropicales del sur'],
        'habitat': 'Aguas abiertas, cerca de la superficie',
        'behavior': 'Casi invisible, tentáculos muy finos'
    },
    {
        'name': 'Barracuda Gigante',
        'thai_name': 'ปลาบาราคูด้ายักษ์ (Pla Barracuda Yak)',
        'image': 'barracuda_gigante.jpg',
        'description': 'Predador agresivo con dientes afilados como navajas. Puede confundir objetos brillantes con presas.',
        'danger_level': 'Alto',
        'areas': ['Aguas costeras', 'Arrecifes'],
        'habitat': 'Aguas abiertas, cerca de arrecifes',
        'behavior': 'Ataca objetos brillantes, cazador oportunista'
    }
]

# Combinar todas las categorías (mantener compatibilidad con código existente)
DANGEROUS_ANIMALS = DANGEROUS_REPTILES + DANGEROUS_INSECTS + DANGEROUS_MAMMALS + DANGEROUS_AQUATIC

# Comida tailandesa organizada por categorías
THAI_MAIN_DISHES = [
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
        'name': 'Massaman Curry',
        'thai_name': 'แกงมัสมั่น',
        'image': 'massaman.jpg',
        'description': 'Curry suave con influencia india, con carne, patatas, cacahuetes y especias aromáticas.',
        'spicy_level': 'Suave',
        'areas': ['Sur de Tailandia', 'Bangkok'],
        'price_range': '60-120 THB'
    },
    {
        'name': 'Pad Krapow',
        'thai_name': 'ผัดกะเพรา',
        'image': 'pad_krapow.jpg',
        'description': 'Carne picada salteada con albahaca sagrada, chiles y ajo. Servido con huevo frito encima.',
        'spicy_level': 'Muy picante',
        'areas': ['Todo el país'],
        'price_range': '35-70 THB'
    },
    {
        'name': 'Green Curry',
        'thai_name': 'แกงเขียวหวาน',
        'image': 'green_curry.jpg',
        'description': 'Curry verde intenso con leche de coco, carne, berenjenas tailandesas y albahaca.',
        'spicy_level': 'Muy picante',
        'areas': ['Todo el país'],
        'price_range': '70-120 THB'
    },
    {
        'name': 'Pad See Ew',
        'thai_name': 'ผัดซีอิ๊ว',
        'image': 'pad_see_ew.jpg',
        'description': 'Fideos anchos salteados con salsa de soja oscura, verduras chinas y carne o tofu.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '40-80 THB'
    },
    {
        'name': 'Tom Kha Gai',
        'thai_name': 'ต้มข่าไก่',
        'image': 'tom_kha_gai.jpg',
        'description': 'Sopa cremosa de pollo con leche de coco, galanga, limoncillo y hojas de lima.',
        'spicy_level': 'Suave',
        'areas': ['Todo el país'],
        'price_range': '60-100 THB'
    },
    {
        'name': 'Larb',
        'thai_name': 'ลาบ',
        'image': 'larb.jpg',
        'description': 'Ensalada de carne picada con hierbas frescas, chile y jugo de lima. Especialidad del noreste.',
        'spicy_level': 'Picante',
        'areas': ['Isaan', 'Norte de Tailandia'],
        'price_range': '50-90 THB'
    },
    {
        'name': 'Gaeng Som',
        'thai_name': 'แกงส้ม',
        'image': 'gaeng_som.jpg',
        'description': 'Curry agrio del sur con pescado, verduras y pasta de tamarindo.',
        'spicy_level': 'Picante',
        'areas': ['Sur de Tailandia'],
        'price_range': '60-100 THB'
    },
    {
        'name': 'Khao Pad',
        'thai_name': 'ข้าวผัด',
        'image': 'khao_pad.jpg',
        'description': 'Arroz frito tailandés con verduras, huevo y tu elección de carne o mariscos.',
        'spicy_level': 'Suave',
        'areas': ['Todo el país'],
        'price_range': '35-80 THB'
    }
]

THAI_DESSERTS = [
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
        'name': 'Thai Coconut Ice Cream',
        'thai_name': 'ไอศกรีมมะพร้าว',
        'image': 'coconut_ice_cream.jpg',
        'description': 'Helado cremoso de coco servido en el propio coco con toppings como maíz, cacahuetes y pan tostado.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '30-60 THB'
    },
    {
        'name': 'Tub Tim Grob',
        'thai_name': 'ทับทิมกรอบ',
        'image': 'tub_tim_grob.jpg',
        'description': 'Postre refrescante con castañas de agua en jarabe, leche de coco y hielo picado.',
        'spicy_level': 'No picante',
        'areas': ['Bangkok', 'Centro de Tailandia'],
        'price_range': '25-50 THB'
    },
    {
        'name': 'Khanom Krok',
        'thai_name': 'ขนมครก',
        'image': 'khanom_krok.jpg',
        'description': 'Pequeños pancakes de coco cocidos en molde especial, crujientes por fuera y cremosos por dentro.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '20-40 THB'
    },
    {
        'name': 'Thong Yip',
        'thai_name': 'ทองหยิบ',
        'image': 'thong_yip.jpg',
        'description': 'Postre real tailandés hecho con yema de huevo y jarabe de azúcar, con forma de flor.',
        'spicy_level': 'No picante',
        'areas': ['Bangkok', 'Ayutthaya'],
        'price_range': '15-30 THB por pieza'
    },
    {
        'name': 'Banana in Coconut Milk',
        'thai_name': 'กล้วยบวชชี',
        'image': 'banana_coconut.jpg',
        'description': 'Plátanos cocidos en leche de coco dulce con un toque de sal. Postre casero tradicional.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '30-50 THB'
    },
    {
        'name': 'Mango with Sweet Sticky Rice',
        'thai_name': 'มะม่วงข้าวเหนียว',
        'image': 'mango_black_rice.jpg',
        'description': 'Variante con arroz negro glutinoso, rico en antioxidantes y con sabor a nuez.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '60-120 THB'
    },
    {
        'name': 'Foi Thong',
        'thai_name': 'ฝอยทอง',
        'image': 'foi_thong.jpg',
        'description': 'Hilos dorados hechos de huevo batido en jarabe de azúcar. Parece pasta de cabello de ángel.',
        'spicy_level': 'No picante',
        'areas': ['Bangkok', 'Centro de Tailandia'],
        'price_range': '20-40 THB'
    }
]

THAI_BEVERAGES = [
    {
        'name': 'Thai Iced Tea',
        'thai_name': 'ชาเย็น',
        'image': 'thai_iced_tea.jpg',
        'description': 'Té negro fuerte con especias, leche condensada y hielo. Color naranja característico.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '20-40 THB'
    },
    {
        'name': 'Thai Iced Coffee',
        'thai_name': 'กาแฟเย็น',
        'image': 'thai_iced_coffee.jpg',
        'description': 'Café fuerte con leche condensada dulce servido con hielo. Energizante y refrescante.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '25-45 THB'
    },
    {
        'name': 'Fresh Coconut Water',
        'thai_name': 'น้ำมะพร้าวสด',
        'image': 'coconut_water.jpg',
        'description': 'Agua de coco fresca directamente del coco joven. Hidratante natural perfecto.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '30-60 THB'
    },
    {
        'name': 'Sugarcane Juice',
        'thai_name': 'น้ำอ้อย',
        'image': 'sugarcane_juice.jpg',
        'description': 'Jugo fresco de caña extraído al momento. Dulce natural y muy refrescante.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '15-30 THB'
    },
    {
        'name': 'Thai Basil Seed Drink',
        'thai_name': 'น้ำเมล็ดแมงลัก',
        'image': 'basil_seed_drink.jpg',
        'description': 'Bebida refrescante con semillas de albahaca que se hinchan, mezclada con jarabe y hielo.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '20-35 THB'
    },
    {
        'name': 'Lemon Grass Tea',
        'thai_name': 'ชาตะไคร้',
        'image': 'lemongrass_tea.jpg',
        'description': 'Infusión caliente o fría de hierba limón. Digestiva y aromática.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '25-40 THB'
    },
    {
        'name': 'Watermelon Juice',
        'thai_name': 'น้ำแตงโม',
        'image': 'watermelon_juice.jpg',
        'description': 'Jugo fresco de sandía, perfecto para el calor tropical. A veces con sal y chile.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '20-40 THB'
    },
    {
        'name': 'Singha Beer',
        'thai_name': 'เบียร์สิงห์',
        'image': 'singha_beer.jpg',
        'description': 'Cerveza lager tailandesa clásica. Refrescante y ligera, perfecta con comida picante.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '60-120 THB'
    },
    {
        'name': 'Chang Beer',
        'thai_name': 'เบียร์ช้าง',
        'image': 'chang_beer.jpg',
        'description': 'Cerveza tailandesa popular con más alcohol. Símbolo del elefante en la etiqueta.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '50-100 THB'
    },
    {
        'name': 'Thai Rum (Sang Som)',
        'thai_name': 'แสงโสม',
        'image': 'sang_som.jpg',
        'description': 'Ron tailandés popular, a menudo mezclado con Coca-Cola y hielo.',
        'spicy_level': 'No picante',
        'areas': ['Todo el país'],
        'price_range': '80-150 THB'
    }
]

# Mantener la compatibilidad con el código existente
THAI_FOOD = THAI_MAIN_DISHES + THAI_DESSERTS + THAI_BEVERAGES

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
        'dangerous_animals': [
            'Cobra Siamés', 'Escorpión Negro Asiático', 'Araña de Saco Amarillo', 
            'Ciempiés Gigante', 'Gecko Tokay', 'Mono Macaco', 'Perro Callejero',
            'Mosquito Dengue', 'Araña Lobo'
        ],
        'dangerous_plants': ['Dieffenbachia', 'Anturio', 'Lirio de Cala', 'Flor de Oleandro'],
        'food_specialties': [
            'Pad Thai', 'Tom Yum Goong', 'Massaman Curry', 'Pad Krapow', 'Green Curry', 'Pad See Ew', 'Tom Kha Gai', 'Khao Pad',
            'Mango Sticky Rice', 'Thai Coconut Ice Cream', 'Tub Tim Grob', 'Thong Yip', 'Foi Thong',
            'Thai Iced Tea', 'Thai Iced Coffee', 'Fresh Coconut Water', 'Singha Beer', 'Chang Beer'
        ],
        'cultural_traditions': ['Wai', 'Respeto a Buda y Monjes', 'Cabeza y Pies', 'La Monarquía'],
        'dangerous_places': ['Patpong Night Market', 'Soi Cowboy', 'Khaosan Road de madrugada', 'Nana Plaza', 'Khlong Toei Slum', 'Callejones de Chinatown de noche']
    },
    'Chiang Mai': {
        'dangerous_animals': [
            'Cobra Rey', 'Escorpión Negro Asiático', 'Mono Macaco', 'Ciempiés Gigante',
            'Elefante Asiático', 'Avispa Gigante Asiática', 'Jabalí', 'Oso Malayo',
            'Leopardo Nebuloso'
        ],
        'dangerous_plants': ['Ricino', 'Flor de Oleandro', 'Dieffenbachia'],
        'food_specialties': [
            'Khao Soi', 'Larb', 'Sai Oua (salchicha norteña)', 'Nam Prik Ong', 'Gaeng Hang Lay',
            'Khanom Krok', 'Banana in Coconut Milk',
            'Lemon Grass Tea', 'Fresh Coconut Water', 'Thai Iced Coffee'
        ],
        'cultural_traditions': ['Loy Krathong', 'Wai', 'Respeto a Buda y Monjes', 'Songkran'],
        'dangerous_places': ['Mercados nocturnos ilegales']
    },
    'Khao Sok': {
        'dangerous_animals': [
            'Cobra Rey', 'Escorpión Negro Asiático', 'Ciempiés Gigante', 'Araña de Saco Amarillo',
            'Pitón Reticulada', 'Elefante Asiático', 'Jabalí', 'Oso Malayo',
            'Leopardo Nebuloso', 'Hormiga Bala'
        ],
        'dangerous_plants': ['Ricino', 'Flor de Oleandro'],
        'food_specialties': [
            'Pescados de río', 'Curry selvático', 'Vegetales locales', 'Tom Yum con hierbas silvestres',
            'Fresh Coconut Water', 'Lemon Grass Tea', 'Sugarcane Juice'
        ],
        'cultural_traditions': ['Wai', 'Respeto a Buda y Monjes'],
        'dangerous_places': []
    },
    'Krabi': {
        'dangerous_animals': [
            'Medusa Caja', 'Escorpión Negro Asiático', 'Mono Macaco', 'Ciempiés Gigante',
            'Cocodrilo de Agua Salada', 'Pez Piedra', 'Serpiente Marina', 'Raya Venenosa',
            'Pulpo de Anillos Azules'
        ],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro', 'Anturio'],
        'food_specialties': [
            'Mariscos frescos', 'Tom Yum Goong', 'Pescado a la parrilla', 'Gaeng Som', 'Curry de cangrejo',
            'Thai Coconut Ice Cream', 'Mango Sticky Rice',
            'Fresh Coconut Water', 'Watermelon Juice', 'Thai Basil Seed Drink'
        ],
        'cultural_traditions': ['Wai', 'Respeto a Buda y Monjes', 'Songkran'],
        'dangerous_places': []
    },
    'Phuket': {
        'dangerous_animals': [
            'Medusa Caja', 'Escorpión Negro Asiático', 'Ciempiés Gigante',
            'Pez Piedra', 'Serpiente Marina', 'Tiburón Toro', 'Raya Venenosa',
            'Medusa Irukandji', 'Barracuda Gigante'
        ],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro', 'Lirio de Cala'],
        'food_specialties': [
            'Mariscos', 'Hokkien Mee', 'Oh Tao (tortilla de ostras)', 'Mee Hokkien', 'Curry Phuket',
            'Thai Coconut Ice Cream', 'Tub Tim Grob',
            'Fresh Coconut Water', 'Singha Beer', 'Chang Beer', 'Thai Rum (Sang Som)'
        ],
        'cultural_traditions': ['Wai', 'Songkran', 'La Monarquía'],
        'dangerous_places': []
    },
    'Koh Phangan': {
        'dangerous_animals': [
            'Medusa Caja', 'Escorpión Negro Asiático', 'Ciempiés Gigante',
            'Pez Piedra', 'Serpiente Marina', 'Raya Venenosa', 'Pez León',
            'Medusa Irukandji'
        ],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro'],
        'food_specialties': [
            'Pescado fresco', 'Curries de mariscos', 'Frutas tropicales', 'Pad Thai playero',
            'Mango Sticky Rice', 'Banana in Coconut Milk',
            'Fresh Coconut Water', 'Thai Rum (Sang Som)', 'Chang Beer', 'Watermelon Juice'
        ],
        'cultural_traditions': ['Full Moon Party', 'Wai', 'Respeto a Buda y Monjes'],
        'dangerous_places': ['Playas solitarias de Koh Phangan']
    },
    'Koh Samui': {
        'dangerous_animals': [
            'Medusa Caja', 'Escorpión Negro Asiático', 'Ciempiés Gigante', 'Mono Macaco',
            'Pez Piedra', 'Serpiente Marina', 'Raya Venenosa', 'Pez León',
            'Barracuda Gigante'
        ],
        'dangerous_plants': ['Fruto del Manzanillo', 'Flor de Oleandro', 'Dieffenbachia'],
        'food_specialties': [
            'Mariscos', 'Som Tam', 'Coconut ice cream', 'Pescado al coco', 'Curry verde con mariscos',
            'Thai Coconut Ice Cream', 'Khanom Krok',
            'Fresh Coconut Water', 'Thai Basil Seed Drink', 'Sugarcane Juice', 'Singha Beer'
        ],
        'cultural_traditions': ['Wai', 'Songkran', 'Respeto a Buda y Monjes'],
        'dangerous_places': []
    }
}