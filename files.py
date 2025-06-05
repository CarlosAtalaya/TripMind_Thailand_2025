# files.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, send_file, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, SharedFile
from datetime import datetime
import os
import uuid
import zipfile
import io
from config import MULTIMEDIA_BASE_PATH, MAX_FOLDER_SIZE, ALLOWED_EXTENSIONS

files = Blueprint('files', __name__)

def get_folder_size(folder_path):
    """Calcula el tamaño total de una carpeta"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def check_storage_limits(file_size):
    """Verifica si hay espacio disponible para el archivo"""
    current_size = get_folder_size(MULTIMEDIA_BASE_PATH)
    if current_size + file_size > MAX_FOLDER_SIZE:
        return False, current_size
    return True, current_size

def format_size(size_bytes):
    """Formatea el tamaño en bytes a una unidad legible"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def ensure_multimedia_folder():
    """Asegura que la carpeta multimedia exista"""
    if not os.path.exists(MULTIMEDIA_BASE_PATH):
        try:
            os.makedirs(MULTIMEDIA_BASE_PATH)
            current_app.logger.info(f"Carpeta multimedia creada en: {MULTIMEDIA_BASE_PATH}")
        except Exception as e:
            current_app.logger.error(f"Error al crear carpeta multimedia: {e}")
            raise

def get_upload_folder():
    """Obtiene la carpeta de subida para la fecha actual"""
    # Asegurar que la carpeta base existe
    ensure_multimedia_folder()
    
    # Crear subcarpeta con la fecha actual
    current_date = datetime.now().strftime('%Y-%m-%d')
    upload_folder = os.path.join(MULTIMEDIA_BASE_PATH, current_date)
    
    # Crear la carpeta si no existe
    if not os.path.exists(upload_folder):
        try:
            os.makedirs(upload_folder)
            current_app.logger.info(f"Carpeta de fecha creada: {upload_folder}")
        except Exception as e:
            current_app.logger.error(f"Error al crear carpeta de fecha: {e}")
            raise
    
    return upload_folder

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_orphaned_records():
    """Limpia registros de archivos que ya no existen en el servidor"""
    orphaned_count = 0
    shared_files = SharedFile.query.all()
    
    for file in shared_files:
        file_path = os.path.join(MULTIMEDIA_BASE_PATH, file.path)
        if not os.path.exists(file_path):
            db.session.delete(file)
            orphaned_count += 1
    
    if orphaned_count > 0:
        try:
            db.session.commit()
            current_app.logger.info(f"Limpiados {orphaned_count} registros huérfanos")
            return orphaned_count
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al limpiar registros huérfanos: {e}")
            return 0
    
    return 0


@files.route('/compartir')
@login_required
def index():
    """Página principal de compartir archivos"""
    # Asegurar que la carpeta existe antes de mostrar archivos
    ensure_multimedia_folder()
    
    # Obtener todos los archivos compartidos ordenados por fecha
    shared_files = SharedFile.query.order_by(SharedFile.upload_date.desc()).all()
    
    # Filtrar archivos que realmente existen en el servidor
    valid_files = []
    orphaned_files = []
    
    for file in shared_files:
        file_path = os.path.join(MULTIMEDIA_BASE_PATH, file.path)
        if os.path.exists(file_path):
            valid_files.append(file)
        else:
            orphaned_files.append(file)
    
    # Opcional: Limpiar registros huérfanos automáticamente
    if orphaned_files:
        for orphan in orphaned_files:
            db.session.delete(orphan)
        try:
            db.session.commit()
            flash(f'Se han limpiado {len(orphaned_files)} registros de archivos no existentes.', 'info')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al limpiar registros huérfanos: {e}")
    
    # Obtener información de almacenamiento
    current_size = get_folder_size(MULTIMEDIA_BASE_PATH)
    
    return render_template('files/index.html', 
                         shared_files=valid_files,
                         current_storage=format_size(current_size),
                         max_storage=format_size(MAX_FOLDER_SIZE),
                         storage_percentage=(current_size / MAX_FOLDER_SIZE) * 100)

@files.route('/compartir/subir', methods=['GET', 'POST'])
@login_required
def upload():
    """Página para subir archivos"""
    if request.method == 'POST':
        # Verificar si hay archivos en la solicitud
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
            
        # CAMBIO: Renombrar la variable para evitar conflicto con el Blueprint
        uploaded_files = request.files.getlist('file')
        description = request.form.get('description', '')
        
        # Calcular el tamaño total de los archivos a subir
        total_upload_size = 0
        for file in uploaded_files:
            if file and file.filename != '':
                file.seek(0, 2)  # Ir al final del archivo
                total_upload_size += file.tell()  # Obtener el tamaño
                file.seek(0)  # Volver al principio
        
        # Verificar límites de almacenamiento
        has_space, current_size = check_storage_limits(total_upload_size)
        if not has_space:
            flash(f'No hay suficiente espacio. Disponible: {format_size(MAX_FOLDER_SIZE - current_size)}, '
                  f'Necesario: {format_size(total_upload_size)}', 'danger')
            return redirect(request.url)
        
        # Procesar cada archivo
        uploaded_count = 0
        for file in uploaded_files:
            if file.filename == '':
                continue
                
            if file and allowed_file(file.filename):
                # Generar un nombre de archivo único
                original_filename = secure_filename(file.filename)
                extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
                unique_filename = f"{uuid.uuid4().hex}.{extension}"
                
                # Obtener la carpeta de destino
                upload_folder = get_upload_folder()
                
                # Guardar el archivo
                file_path = os.path.join(upload_folder, unique_filename)
                try:
                    file.save(file_path)
                    
                    # Registrar en la base de datos
                    shared_file = SharedFile(
                        filename=unique_filename,
                        original_filename=original_filename,
                        path=os.path.join(datetime.now().strftime('%Y-%m-%d'), unique_filename),
                        filesize=os.path.getsize(file_path),
                        mimetype=file.content_type,
                        user_id=current_user.id,
                        description=description
                    )
                    
                    db.session.add(shared_file)
                    uploaded_count += 1
                except Exception as e:
                    current_app.logger.error(f"Error al guardar archivo {original_filename}: {e}")
                    flash(f'Error al guardar el archivo {original_filename}', 'danger')
            else:
                flash(f'El formato del archivo {file.filename} no está permitido', 'warning')
        
        if uploaded_count > 0:
            try:
                db.session.commit()
                flash(f'Se han subido {uploaded_count} archivos correctamente', 'success')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error al guardar en base de datos: {e}")
                flash('Error al guardar información en base de datos', 'danger')
            return redirect(url_for('files.index'))
    
    # Obtener información de almacenamiento para la página de subida
    current_size = get_folder_size(MULTIMEDIA_BASE_PATH)
    
    return render_template('files/upload.html',
                         current_storage=format_size(current_size),
                         max_storage=format_size(MAX_FOLDER_SIZE),
                         available_storage=format_size(MAX_FOLDER_SIZE - current_size))

@files.route('/compartir/descargar/<int:file_id>')
@login_required
def download(file_id):
    """Descargar un archivo compartido"""
    shared_file = SharedFile.query.get_or_404(file_id)
    date_folder = shared_file.path.split('/')[0]
    filename = shared_file.filename
    
    return send_from_directory(
        os.path.join(MULTIMEDIA_BASE_PATH, date_folder),
        filename,
        as_attachment=True,
        download_name=shared_file.original_filename
    )

@files.route('/compartir/download-multiple', methods=['POST'])
@login_required
def download_multiple():
    """Crear un ZIP con múltiples archivos seleccionados"""
    try:
        data = request.get_json()
        file_ids = data.get('file_ids', [])
        
        if not file_ids:
            return jsonify({'success': False, 'error': 'No se seleccionaron archivos'}), 400
        
        # Obtener archivos de la base de datos
        files = SharedFile.query.filter(SharedFile.id.in_(file_ids)).all()
        
        if not files:
            return jsonify({'success': False, 'error': 'No se encontraron archivos'}), 404
        
        # Crear ZIP en memoria
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                file_path = os.path.join(MULTIMEDIA_BASE_PATH, file.path)
                if os.path.exists(file_path):
                    # Añadir archivo al ZIP con nombre único para evitar conflictos
                    safe_username = file.user.username.replace(' ', '_')
                    filename = f"{safe_username}_{file.original_filename}"
                    zf.write(file_path, filename)
        
        memory_file.seek(0)
        
        # Crear nombre del ZIP
        if len(files) == 1:
            zip_name = f"{files[0].original_filename}.zip"
        else:
            zip_name = f"archivos_seleccionados_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_name
        )
        
    except Exception as e:
        current_app.logger.error(f"Error en descarga múltiple: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
    
@files.route('/compartir/download-all', methods=['GET'])
@login_required
def download_all():
    """Descargar TODOS los archivos en un ZIP"""
    try:
        # Obtener TODOS los archivos de la base de datos
        files = SharedFile.query.order_by(SharedFile.upload_date.desc()).all()
        
        if not files:
            flash('No hay archivos para descargar', 'warning')
            return redirect(url_for('files.index'))
        
        # Crear ZIP en memoria
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                file_path = os.path.join(MULTIMEDIA_BASE_PATH, file.path)
                if os.path.exists(file_path):
                    # Crear nombre único: fecha_usuario_nombrearchivo
                    date_str = file.upload_date.strftime('%Y-%m-%d')
                    safe_username = file.user.username.replace(' ', '_')
                    filename = f"{date_str}_{safe_username}_{file.original_filename}"
                    zf.write(file_path, filename)
        
        memory_file.seek(0)
        
        zip_name = f"todos_los_archivos_{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_name
        )
        
    except Exception as e:
        current_app.logger.error(f"Error en descarga total: {e}")
        flash('Error al preparar la descarga', 'danger')
        return redirect(url_for('files.index'))

@files.route('/compartir/download-by-date/<date>')
@login_required
def download_by_date(date):
    """Descargar todos los archivos de una fecha específica en ZIP - VERSIÓN CORREGIDA"""
    try:
        # Validar formato de fecha
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido', 'danger')
            return redirect(url_for('files.index'))
        
        # Obtener archivos de esa fecha - CONSULTA CORREGIDA
        files = SharedFile.query.filter(
            db.func.date(SharedFile.upload_date) == date_obj
        ).all()
        
        if not files:
            flash(f'No hay archivos para la fecha {date}', 'warning')
            return redirect(url_for('files.index'))
        
        # Crear ZIP en memoria
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                file_path = os.path.join(MULTIMEDIA_BASE_PATH, file.path)
                if os.path.exists(file_path):
                    # Crear nombre único para evitar conflictos
                    safe_username = file.user.username.replace(' ', '_')
                    filename = f"{safe_username}_{file.original_filename}"
                    zf.write(file_path, filename)
        
        memory_file.seek(0)
        
        zip_name = f"archivos_{date}.zip"
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_name
        )
        
    except Exception as e:
        current_app.logger.error(f"Error en descarga por fecha: {e}")
        flash('Error al preparar la descarga', 'danger')
        return redirect(url_for('files.index'))

@files.route('/compartir/eliminar/<int:file_id>', methods=['POST'])
@login_required
def delete(file_id):
    """Eliminar un archivo compartido"""
    shared_file = SharedFile.query.get_or_404(file_id)
    
    # Verificar si el usuario actual es el propietario o un administrador
    if shared_file.user_id != current_user.id and not current_user.is_admin:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'No tienes permisos para eliminar este archivo'}), 403
        else:
            flash('No tienes permisos para eliminar este archivo', 'danger')
            return redirect(url_for('files.index'))
    
    try:
        # Eliminar el archivo físico
        file_path = os.path.join(MULTIMEDIA_BASE_PATH, shared_file.path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Eliminar el registro de la base de datos
        db.session.delete(shared_file)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Archivo eliminado correctamente'})
        else:
            flash('Archivo eliminado correctamente', 'success')
            return redirect(url_for('files.index'))
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            flash(f'Error al eliminar el archivo: {str(e)}', 'danger')
            return redirect(url_for('files.index'))

@files.route('/compartir/preview/<int:file_id>')
@login_required
def preview(file_id):
    """Previsualizar un archivo (para imágenes)"""
    shared_file = SharedFile.query.get_or_404(file_id)
    date_folder = shared_file.path.split('/')[0]
    filename = shared_file.filename
    
    # Verificar que el archivo existe
    file_path = os.path.join(MULTIMEDIA_BASE_PATH, date_folder, filename)
    if not os.path.exists(file_path):
        # Opcional: Eliminar el registro huérfano
        db.session.delete(shared_file)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        
        flash('El archivo no existe en el servidor', 'danger')
        return redirect(url_for('files.index'))
    
    # Para imágenes, servir sin forzar descarga
    return send_from_directory(
        os.path.join(MULTIMEDIA_BASE_PATH, date_folder),
        filename,
        as_attachment=False  # Esto permite que se muestre en el navegador
    )

@files.route('/admin/cleanup-orphaned')
@login_required
def admin_cleanup_orphaned():
    """Limpia manualmente los registros huérfanos (solo admin)"""
    from auth import admin_required
    
    if not current_user.is_admin:
        flash('Se requieren permisos de administrador', 'danger')
        return redirect(url_for('files.index'))
    
    count = cleanup_orphaned_records()
    if count > 0:
        flash(f'Se han limpiado {count} registros de archivos no existentes.', 'success')
    else:
        flash('No se encontraron registros huérfanos.', 'info')
    
    return redirect(url_for('files.index'))

@files.route('/api/storage-info')
@login_required
def storage_info():
    """API para obtener información de almacenamiento"""
    current_size = get_folder_size(MULTIMEDIA_BASE_PATH)
    return jsonify({
        'current_size': current_size,
        'current_size_formatted': format_size(current_size),
        'max_size': MAX_FOLDER_SIZE,
        'max_size_formatted': format_size(MAX_FOLDER_SIZE),
        'available_size': MAX_FOLDER_SIZE - current_size,
        'available_size_formatted': format_size(MAX_FOLDER_SIZE - current_size),
        'percentage_used': (current_size / MAX_FOLDER_SIZE) * 100
    })