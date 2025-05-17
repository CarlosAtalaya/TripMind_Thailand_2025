# diary.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, DiaryEntry
from datetime import datetime
import json
import os

diary = Blueprint('diary', __name__)

# Función para guardar todas las entradas en un JSON como backup
def backup_entries_to_json():
    try:
        # Obtener todas las entradas
        entries = DiaryEntry.query.all()
        
        # Crear directorio de backup si no existe
        backup_dir = 'data/backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Preparar datos para JSON
        entries_data = []
        for entry in entries:
            entries_data.append({
                'user_id': entry.user_id,
                'username': entry.user.username,
                'name': entry.user.name,
                'date': entry.date.strftime('%Y-%m-%d %H:%M:%S'),
                'content': entry.content
            })
        
        # Guardar en archivo JSON
        backup_file = os.path.join(backup_dir, 'diary_entries.json')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(entries_data, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(f"Error al hacer backup de entradas: {e}")
        return False

@diary.route('/diario')
@login_required
def index():
    """Página principal del diario"""
    # Obtener entradas del usuario actual
    entries = DiaryEntry.query.filter_by(user_id=current_user.id).order_by(DiaryEntry.date.desc()).all()
    return render_template('diary/index.html', entries=entries)

@diary.route('/diario/nueva', methods=['GET', 'POST'])
@login_required
def new_entry():
    """Página para crear una nueva entrada"""
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content or len(content.strip()) == 0:
            flash('El contenido no puede estar vacío', 'danger')
            return redirect(url_for('diary.new_entry'))
        
        # Crear nueva entrada
        entry = DiaryEntry(
            user_id=current_user.id,
            content=content
        )
        
        db.session.add(entry)
        
        try:
            db.session.commit()
            # Hacer backup en JSON
            backup_entries_to_json()
            flash('Entrada guardada correctamente', 'success')
            return redirect(url_for('diary.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar la entrada: {e}', 'danger')
    
    return render_template('diary/entry_form.html')

@diary.route('/diario/editar/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    """Página para editar una entrada existente"""
    entry = DiaryEntry.query.get_or_404(entry_id)
    
    # Verificar que la entrada pertenece al usuario actual
    if entry.user_id != current_user.id:
        flash('No tienes permiso para editar esta entrada', 'danger')
        return redirect(url_for('diary.index'))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not content or len(content.strip()) == 0:
            flash('El contenido no puede estar vacío', 'danger')
            return redirect(url_for('diary.edit_entry', entry_id=entry_id))
        
        # Actualizar entrada
        entry.content = content
        
        try:
            db.session.commit()
            # Hacer backup en JSON
            backup_entries_to_json()
            flash('Entrada actualizada correctamente', 'success')
            return redirect(url_for('diary.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la entrada: {e}', 'danger')
    
    return render_template('diary/entry_form.html', entry=entry)

@diary.route('/diario/eliminar/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    """Eliminar una entrada"""
    # Esta función está deshabilitada para evitar la eliminación de entradas
    flash('La eliminación de entradas de diario ha sido deshabilitada', 'warning')
    return redirect(url_for('diary.index'))