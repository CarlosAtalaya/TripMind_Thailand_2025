# files.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, SharedFile
from datetime import datetime
import os
import uuid

files = Blueprint('files', __name__)

def get_upload_folder():
    """Obtiene la carpeta de subida para la fecha actual"""
    base_path = '/home/carlos/Documentos/Multimedia_Tailandia2025'
    current_date = datetime.now().strftime('%Y-%m-%d')
    upload_folder = os.path.join(base_path, current_date)
    
    # Crear la carpeta si no existe
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    return upload_folder

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'pdf', 'zip', 'rar'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files.route('/compartir')
@login_required
def index():
    """Página principal de compartir archivos"""
    # Obtener todos los archivos compartidos ordenados por fecha
    shared_files = SharedFile.query.order_by(SharedFile.upload_date.desc()).all()
    return render_template('files/index.html', shared_files=shared_files)

@files.route('/compartir/subir', methods=['GET', 'POST'])
@login_required
def upload():
    """Página para subir archivos"""
    if request.method == 'POST':
        # Verificar si hay archivos en la solicitud
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)
            
        files = request.files.getlist('file')
        description = request.form.get('description', '')
        
        # Procesar cada archivo
        uploaded_count = 0
        for file in files:
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
            else:
                flash(f'El formato del archivo {file.filename} no está permitido', 'warning')
        
        if uploaded_count > 0:
            db.session.commit()
            flash(f'Se han subido {uploaded_count} archivos correctamente', 'success')
            return redirect(url_for('files.index'))
    
    return render_template('files/upload.html')

@files.route('/compartir/descargar/<int:file_id>')
@login_required
def download(file_id):
    """Descargar un archivo compartido"""
    shared_file = SharedFile.query.get_or_404(file_id)
    date_folder = shared_file.path.split('/')[0]
    filename = shared_file.filename
    
    return send_from_directory(
        os.path.join('/home/carlos/Documentos/Multimedia_Tailandia2025', date_folder),
        filename,
        as_attachment=True,
        download_name=shared_file.original_filename
    )

@files.route('/compartir/eliminar/<int:file_id>', methods=['POST'])
@login_required
def delete(file_id):
    """Eliminar un archivo compartido"""
    shared_file = SharedFile.query.get_or_404(file_id)
    
    # Verificar si el usuario actual es el propietario o un administrador
    if shared_file.user_id != current_user.id and not current_user.is_admin:
        flash('No tienes permisos para eliminar este archivo', 'danger')
        return redirect(url_for('files.index'))
    
    try:
        # Eliminar el archivo físico
        file_path = os.path.join('/home/carlos/Documentos/Multimedia_Tailandia2025', shared_file.path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Eliminar el registro de la base de datos
        db.session.delete(shared_file)
        db.session.commit()
        
        flash('Archivo eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el archivo: {str(e)}', 'danger')
    
    return redirect(url_for('files.index'))