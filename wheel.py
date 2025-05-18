# wheel.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, AppConfig
from auth import admin_required

wheel = Blueprint('wheel', __name__)

@wheel.route('/ruleta')
@login_required
def index():
    """Página principal de la ruleta"""
    return render_template('wheel/index.html')

# Cambiar esta ruta para que funcione con la URL completa
@wheel.route('/api/wheel/users')
@login_required
def get_users():
    """API para obtener los usuarios activos para la ruleta"""
    try:
        # Obtener todos los usuarios activos
        active_users = User.query.filter_by(is_active_member=True).all()
        
        users_data = []
        for user in active_users:
            users_data.append({
                'id': user.id, 
                'name': user.name
            })
        
        return jsonify({
            'success': True,
            'users': users_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Cambiar esta ruta para que funcione con la URL completa
@wheel.route('/api/wheel/title')
@login_required
def get_wheel_title():
    """API para obtener el título personalizado de la ruleta"""
    try:
        title = AppConfig.get_value('wheel_title', '¿A quién le toca?')
        return jsonify({
            'success': True,
            'title': title
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wheel.route('/admin/wheel/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_settings():
    """Página de configuración de la ruleta para administradores"""
    if request.method == 'POST':
        wheel_title = request.form.get('wheel_title', '¿A quién le toca?')
        
        try:
            AppConfig.set_value('wheel_title', wheel_title, 'Título personalizado para la ruleta')
            flash('Configuración de la ruleta actualizada correctamente', 'success')
            return redirect(url_for('auth.admin_panel'))
        except Exception as e:
            flash(f'Error al guardar la configuración: {e}', 'danger')
    
    # Obtener la configuración actual
    current_title = AppConfig.get_value('wheel_title', '¿A quién le toca?')
    
    return render_template('wheel/admin_settings.html', current_title=current_title)