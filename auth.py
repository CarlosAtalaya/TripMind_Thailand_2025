# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db, CountdownEvent
from functools import wraps
from datetime import datetime
import pytz

auth = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Se requieren permisos de administrador para acceder a esta página', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if not user or not user.check_password(password):
            flash('Usuario o contraseña incorrectos, por favor intenta de nuevo', 'danger')
            return redirect(url_for('auth.login'))
            
        # Si todo está bien, iniciar sesión
        login_user(user, remember=remember)
        flash(f'Bienvenido, {user.name}!', 'success')
        
        # Redirigir a la página que intentaba acceder o a la página principal
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
        
    current_date = datetime.now(pytz.UTC)
    return render_template('login.html', current_date=current_date)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin_panel():
    users = User.query.all()
    current_date = datetime.now(pytz.UTC)
    return render_template('admin.html', users=users, current_date=current_date)

@auth.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        is_admin = True if request.form.get('is_admin') else False
        is_active_member = True if request.form.get('is_active_member') else False
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('auth.add_user'))
            
        # Crear nuevo usuario
        new_user = User(
            username=username, 
            name=name, 
            phone=phone, 
            is_admin=is_admin,
            is_active_member=is_active_member
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('auth.admin_panel'))
        
    current_date = datetime.now(pytz.UTC)
    return render_template('user_form.html', action='add', current_date=current_date)


@auth.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        user.is_admin = True if request.form.get('is_admin') else False
        user.is_active_member = True if request.form.get('is_active_member') else False
        
        # Actualizar contraseña solo si se proporciona una nueva
        password = request.form.get('password')
        if password and password.strip():
            user.set_password(password)
            
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('auth.admin_panel'))
        
    current_date = datetime.now(pytz.UTC)
    return render_template('user_form.html', action='edit', user=user, current_date=current_date)

@auth.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # No permitir eliminar al propio usuario
    if user.id == current_user.id:
        flash('No puedes eliminarte a ti mismo', 'danger')
        return redirect(url_for('auth.admin_panel'))
        
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('auth.admin_panel'))

# Añadir esta nueva función en auth.py

@auth.route('/admin/user/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Activar o desactivar un usuario"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    activate = data.get('activate', True)
    
    # No permitir desactivar al propio usuario
    if user.id == current_user.id and not activate:
        return jsonify({
            'success': False,
            'error': 'No puedes desactivarte a ti mismo'
        }), 400
    
    try:
        user.is_active_member = activate
        db.session.commit()
        
        action = "activado" if activate else "desactivado"
        return jsonify({
            'success': True,
            'message': f'Usuario {action} exitosamente'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@auth.route('/admin/countdown', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_countdown():
    countdown = CountdownEvent.query.first()
    inactive_users = User.query.filter_by(is_active_member=False).all()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            event_date = request.form.get('event_date')
            event_time = request.form.get('event_time')
            user_id = request.form.get('user_id')
            
            try:
                # Combinar fecha y hora
                event_datetime = datetime.strptime(f"{event_date} {event_time}", '%Y-%m-%d %H:%M')
                
                # Crear o actualizar el evento
                if countdown:
                    countdown.event_datetime = event_datetime
                    countdown.user_to_activate_id = user_id if user_id else None
                    countdown.is_active = True
                else:
                    countdown = CountdownEvent(
                        event_datetime=event_datetime,
                        user_to_activate_id=user_id if user_id else None,
                        is_active=True
                    )
                    db.session.add(countdown)
                
                db.session.commit()
                flash('Contador activado correctamente', 'success')
                
            except Exception as e:
                flash(f'Error al configurar el contador: {e}', 'danger')
                
        elif action == 'deactivate':
            if countdown:
                countdown.is_active = False
                db.session.commit()
                flash('Contador desactivado', 'info')
    
    return render_template('admin/countdown.html', 
                         countdown=countdown, 
                         inactive_users=inactive_users)

@auth.route('/api/countdown/status')
def countdown_status():
    """API para obtener el estado del contador"""
    try:
        countdown = CountdownEvent.query.filter_by(is_active=True).first()
        
        if not countdown:
            return jsonify({'active': False})
        
        now = datetime.now()
        event_time = countdown.event_datetime
        
        # Verificar si ya pasó el evento
        if now >= event_time:
            # Verificar si han pasado menos de 1 hora
            time_diff = (now - event_time).total_seconds()
            
            if time_diff <= 3600:  # 1 hora = 3600 segundos
                # Activar el usuario si existe y aún no está activado
                user_name = None
                if countdown.user_to_activate_id:
                    user = User.query.get(countdown.user_to_activate_id)
                    if user:
                        user_name = user.name
                        if not user.is_active_member and time_diff < 60:  # Solo la primera vez
                            user.is_active_member = True
                            db.session.commit()
                
                return jsonify({
                    'active': True,
                    'event_happened': True,
                    'message': countdown.message,
                    'new_user': user_name
                })
            else:
                # Desactivar el contador después de 1 hora
                countdown.is_active = False
                db.session.commit()
                return jsonify({'active': False})
        
        # El evento aún no ha ocurrido
        time_remaining = (event_time - now).total_seconds()
        
        return jsonify({
            'active': True,
            'event_happened': False,
            'time_remaining': int(time_remaining),
            'event_datetime': event_time.isoformat()
        })
        
    except Exception as e:
        print(f"Error en countdown_status: {e}")
        return jsonify({'active': False, 'error': str(e)}), 500