# 🌏 TravelBoard - El Viaje de la Conquista Tailandia 2025

Una aplicación web personalizada para gestionar y documentar un viaje grupal a Tailandia. Desarrollada con Flask y diseñada para proporcionar funcionalidades útiles y divertidas para el grupo de viajeros.

## ✨ Características

### 📅 Gestión de Itinerario
- Vista detallada del itinerario por regiones
- Información de alojamiento y transporte
- Actividades planificadas por día
- Barra de progreso del viaje

### 🌤️ Información del Clima
- Pronóstico meteorológico en tiempo real para cada región
- Integración con OpenMeteo API
- Actualización automática cada hora

### 📰 Noticias Relevantes
- Agregador de noticias relacionadas con las regiones del viaje
- Filtrado por palabras clave de seguridad y turismo
- Actualización cada 30 minutos

### 📸 Compartir Archivos
- Sistema para subir y compartir fotos/videos del viaje
- Organización automática por fecha
- Soporte para múltiples formatos (JPG, PNG, MP4, PDF, etc.)

### 🏆 Sistema de Votaciones
- Categorías divertidas para votar entre compañeros
- Sistema de puntos y rankings
- Resultados en tiempo real

### 📖 Diario Personal
- Diario privado para cada viajero
- Solo visible por el propio usuario
- Backup automático en JSON

### 💩 Contador de Cacas
- Funcionalidad humorística para llevar un recuento
- Contador individual para cada viajero
- Visualización en la página principal

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip

### Pasos de Instalación

1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd TripMind_Thailand_2025
```

2. Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (opcional)
```bash
export SECRET_KEY="tu_clave_secreta"
export NEWS_API_KEY="tu_api_key"  # Si tienes una API key propia
```

5. Inicializar la base de datos (primera vez)
```bash
python init_db.py
```

6. Iniciar la aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### ⚠️ Nota sobre la Base de Datos
- La base de datos SQLite se crea automáticamente en la carpeta `instance/`
- Esta carpeta **NO debe subirse al repositorio** (está en .gitignore)
- Cada instalación tendrá su propia base de datos local
- Para respaldar datos importantes, usa la funcionalidad de backup de la aplicación

## 📁 Estructura del Proyecto

```
TripMind_Thailand_2025/
├── app.py                 # Aplicación principal Flask
├── config.py             # Configuración de la aplicación
├── models.py             # Modelos de base de datos
├── auth.py               # Sistema de autenticación
├── files.py              # Gestión de archivos compartidos
├── votes.py              # Sistema de votaciones
├── diary.py              # Diario personal
├── poop_counter.py       # Contador de cacas
├── requirements.txt      # Dependencias Python
├── data/
│   ├── itineraries/      # Archivos YAML de itinerarios
│   └── backups/          # Backups de datos
├── services/
│   ├── itinerary.py      # Servicio de itinerario
│   ├── weather.py        # Servicio de clima
│   └── news.py           # Servicio de noticias
├── static/
│   ├── css/              # Estilos CSS
│   └── js/               # Scripts JavaScript
└── templates/            # Plantillas HTML Jinja2
```

## 🔧 Configuración

### Primer Usuario Administrador
Al iniciar la aplicación por primera vez, se mostrará una página de configuración para crear el primer usuario administrador.

### Gestión de Usuarios
Los administradores pueden:
- Crear nuevos usuarios
- Editar usuarios existentes
- Asignar permisos de administrador

### Itinerario
El itinerario se configura en `data/itineraries/thailand_2025.yaml`. Incluye:
- Regiones y fechas
- Alojamientos
- Transportes
- Actividades
- Información de emergencia

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, JavaScript vanilla
- **Base de datos**: SQLite
- **APIs**: OpenMeteo (clima), RSS feeds (noticias)
- **Autenticación**: Flask-Login
- **Formato de datos**: YAML, JSON

## 📱 Diseño Responsive

La aplicación está optimizada para:
- Escritorio
- Tablets
- Móviles

## 🔒 Seguridad

- Autenticación de usuarios
- Sesiones seguras
- Validación de archivos subidos
- Permisos basados en roles

## 👥 Contribuir

Si eres parte del grupo de viaje y quieres contribuir:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y de uso exclusivo para el grupo de viaje "El Viaje de la Conquista Tailandia 2025".

## 🙏 Agradecimientos

- A todos los viajeros por hacer posible este viaje
- OpenMeteo por proporcionar datos meteorológicos gratuitos
- La comunidad Flask por la excelente documentación

---

Desarrollado con ❤️ para el mejor grupo de viaje