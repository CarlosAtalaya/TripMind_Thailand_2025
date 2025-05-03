# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
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
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('auth.add_user'))
            
        # Crear nuevo usuario
        new_user = User(username=username, name=name, phone=phone, is_admin=is_admin)
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