# daily_photos.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User
from datetime import datetime
import os
import pytz
from config import (
    MULTIMEDIA_BASE_PATH,
    DAILY_PHOTOS_FOLDER,
    DAILY_PHOTOS_ALLOWED_EXTENSIONS,
    DAILY_PHOTOS_MAX_SIZE,
    DAILY_DEADLINE_HOUR,
    THAILAND_TZ
)
from PIL import Image
import uuid

daily_photos = Blueprint('daily_photos', __name__)

# Configuración específica para fotos diarias
DAILY_PHOTOS_FULL_PATH = os.path.join(MULTIMEDIA_BASE_PATH, DAILY_PHOTOS_FOLDER)
THAILAND_TZ_OBJ = pytz.timezone(THAILAND_TZ)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in DAILY_PHOTOS_ALLOWED_EXTENSIONS

def ensure_daily_photos_folder():
    """Asegura que la carpeta base de fotos diarias exista"""
    if not os.path.exists(DAILY_PHOTOS_FULL_PATH):
        try:
            os.makedirs(DAILY_PHOTOS_FULL_PATH)
        except Exception as e:
            print(f"Error al crear carpeta de fotos diarias: {e}")
            raise

def get_daily_folder(date=None):
    """Obtiene la carpeta para las fotos del día"""
    ensure_daily_photos_folder()
    
    if date is None:
        date = datetime.now(THAILAND_TZ_OBJ)
    
    # Crear subcarpeta con la fecha actual
    date_folder = date.strftime('%Y-%m-%d')
    folder_path = os.path.join(DAILY_PHOTOS_FULL_PATH, date_folder)
    
    # Crear la carpeta si no existe
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except Exception as e:
            print(f"Error al crear carpeta de fecha: {e}")
            raise
    
    return folder_path

def get_user_photo_filename(user_id, user_name, extension='jpg'):
    """Genera el nombre del archivo para la foto del usuario"""
    return f"{user_name}_{datetime.now(THAILAND_TZ_OBJ).strftime('%Y-%m-%d')}.{extension}"

def has_user_uploaded_today(user_id, user_name):
    """Verifica si el usuario ya ha subido una foto hoy"""
    today_folder = get_daily_folder()
    date_str = datetime.now(THAILAND_TZ_OBJ).strftime('%Y-%m-%d')
    
    # Buscar si existe algún archivo del usuario para hoy
    for ext in DAILY_PHOTOS_ALLOWED_EXTENSIONS:
        filename = f"{user_name}_{date_str}.{ext}"
        if os.path.exists(os.path.join(today_folder, filename)):
            return True
    return False

def is_upload_time_valid():
    """Verifica si aún se pueden subir fotos (antes de las 8 PM hora tailandesa)"""
    current_time = datetime.now(THAILAND_TZ_OBJ)
    return current_time.hour < DAILY_DEADLINE_HOUR

def get_all_daily_photos(date=None):
    """Obtiene todas las fotos del día especificado"""
    if date is None:
        date = datetime.now(THAILAND_TZ_OBJ)
    
    date_str = date.strftime('%Y-%m-%d')
    folder_path = get_daily_folder(date)
    
    photos = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if any(filename.endswith(f'.{ext}') for ext in DAILY_PHOTOS_ALLOWED_EXTENSIONS):
                # Extraer el nombre del usuario del filename
                parts = filename.split('_')
                if len(parts) >= 2:  # Formato: nombre_fecha.ext
                    user_name = parts[0]
                    user = User.query.filter_by(name=user_name).first()
                    if user:
                        photos.append({
                            'user_id': user.id,
                            'user_name': user.name,
                            'filename': filename,
                            'path': os.path.join(date_str, filename),
                            'url': url_for('daily_photos.get_photo', date=date_str, filename=filename)
                        })
    
    return photos

@daily_photos.route('/daily-photo/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Página para subir la foto diaria"""
    # Verificar si aún se puede subir
    if not is_upload_time_valid():
        flash('Ya pasó la hora límite para subir fotos (8 PM hora de Tailandia)', 'warning')
        return redirect(url_for('votes.index'))
    
    # Verificar si ya subió hoy
    if has_user_uploaded_today(current_user.id, current_user.name):
        flash('Ya has subido tu foto de hoy', 'info')
        return redirect(url_for('votes.index'))
    
    if request.method == 'POST':
        # Verificar si hay archivo en la solicitud
        if 'photo' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        
        file = request.files['photo']
        
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Obtener la extensión del archivo
                extension = file.filename.rsplit('.', 1)[1].lower()
                
                # Generar nombre del archivo
                filename = get_user_photo_filename(current_user.id, current_user.name, extension)
                
                # Obtener carpeta del día
                folder_path = get_daily_folder()
                file_path = os.path.join(folder_path, filename)
                
                # Guardar archivo temporalmente
                temp_path = file_path + '.tmp'
                file.save(temp_path)
                
                # Verificar tamaño del archivo
                if os.path.getsize(temp_path) > DAILY_PHOTOS_MAX_SIZE:
                    os.remove(temp_path)
                    flash('El archivo es demasiado grande. Máximo 25 MB.', 'danger')
                    return redirect(request.url)
                
                # Procesar imagen (opcional: redimensionar si es muy grande)
                try:
                    with Image.open(temp_path) as img:
                        # Convertir a RGB si es necesario (para compatibilidad con JPEG)
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Redimensionar si es demasiado grande
                        max_dimension = 1920
                        if img.width > max_dimension or img.height > max_dimension:
                            img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                        
                        # Guardar imagen procesada
                        img.save(file_path, quality=85, optimize=True)
                    
                    # Eliminar archivo temporal
                    os.remove(temp_path)
                except Exception as e:
                    print(f"Error procesando imagen: {e}")
                    # Si falla el procesamiento, usar el archivo original
                    if os.path.exists(temp_path):
                        os.rename(temp_path, file_path)
                
                flash('¡Foto subida con éxito!', 'success')
                return redirect(url_for('votes.index'))
                
            except Exception as e:
                print(f"Error al guardar foto: {e}")
                flash('Error al guardar la foto', 'danger')
                return redirect(request.url)
        else:
            flash('Formato de archivo no permitido. Usa JPG, PNG, GIF o WebP', 'danger')
            return redirect(request.url)
    
    # GET request
    current_time = datetime.now(THAILAND_TZ_OBJ)
    deadline_time = current_time.replace(hour=DAILY_DEADLINE_HOUR, minute=0, second=0, microsecond=0)
    time_remaining = deadline_time - current_time
    
    return render_template('daily_photos/upload.html',
                          time_remaining=time_remaining,
                          deadline_hour=DAILY_DEADLINE_HOUR)

@daily_photos.route('/daily-photo/gallery')
@login_required
def gallery():
    """Galería de fotos del día"""
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=THAILAND_TZ_OBJ)
        except:
            date = datetime.now(THAILAND_TZ_OBJ)
    else:
        date = datetime.now(THAILAND_TZ_OBJ)
    
    photos = get_all_daily_photos(date)
    
    return render_template('daily_photos/gallery.html',
                          photos=photos,
                          date=date)

@daily_photos.route('/daily-photo/<date>/<filename>')
@login_required
def get_photo(date, filename):
    """Servir una foto específica"""
    folder_path = os.path.join(DAILY_PHOTOS_FULL_PATH, date)
    return send_from_directory(folder_path, filename)

@daily_photos.route('/daily-photo/api/photos')
@login_required
def api_get_photos():
    """API para obtener las fotos del día"""
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=THAILAND_TZ_OBJ)
        except:
            date = datetime.now(THAILAND_TZ_OBJ)
    else:
        date = datetime.now(THAILAND_TZ_OBJ)
    
    photos = get_all_daily_photos(date)
    return jsonify({'success': True, 'photos': photos})

@daily_photos.route('/daily-photo/api/status')
@login_required
def api_status():
    """API para obtener el estado de subida del usuario actual"""
    current_time = datetime.now(THAILAND_TZ_OBJ)
    deadline_time = current_time.replace(hour=DAILY_DEADLINE_HOUR, minute=0, second=0, microsecond=0)
    
    return jsonify({
        'success': True,
        'has_uploaded': has_user_uploaded_today(current_user.id, current_user.name),
        'can_upload': is_upload_time_valid(),
        'current_time': current_time.isoformat(),
        'deadline_time': deadline_time.isoformat(),
        'time_remaining': str(deadline_time - current_time) if current_time < deadline_time else None
    })
