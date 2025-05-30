from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Survey, SurveyOption, SurveyResponse, User
from auth import admin_required
from datetime import datetime, timedelta

survey = Blueprint('survey', __name__)

@survey.route('/encuestas')
@login_required
def index():
    """Página principal de encuestas"""
    # Obtener encuestas donde el usuario está autorizado O es admin
    if current_user.is_admin:
        # Admins pueden ver todas las encuestas activas
        active_surveys = Survey.query.filter(Survey.is_active == True).all()
    else:
        # Usuarios normales solo ven encuestas donde están autorizados
        active_surveys = Survey.query.filter(
            Survey.is_active == True,
            Survey.authorized_users.any(id=current_user.id)
        ).all()
    
    # Obtener encuestas ya respondidas por el usuario
    responded_surveys = []
    for active_survey in active_surveys:
        response = SurveyResponse.query.filter_by(
            survey_id=active_survey.id,
            user_id=current_user.id
        ).first()
        
        if response:
            responded_surveys.append(active_survey.id)
    
    # Para admins: obtener todas las encuestas para gestión
    all_surveys = None
    if current_user.is_admin:
        all_surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    
    return render_template('survey/index.html', 
                          active_surveys=active_surveys,
                          responded_surveys=responded_surveys,
                          all_surveys=all_surveys)

@survey.route('/encuestas/<int:survey_id>')
@login_required
def view_survey(survey_id):
    """Ver y responder a una encuesta específica"""
    # Obtener la encuesta
    survey_data = Survey.query.get_or_404(survey_id)
    
    # Verificar acceso: admin O usuario autorizado
    is_authorized = current_user.is_admin or current_user in survey_data.authorized_users
    
    if not is_authorized:
        flash('No tienes permiso para acceder a esta encuesta', 'danger')
        return redirect(url_for('survey.index'))
    
    # Verificar si el usuario ya respondió
    existing_response = SurveyResponse.query.filter_by(
        survey_id=survey_id,
        user_id=current_user.id
    ).first()
    
    # Verificar si la encuesta está cerrada
    is_closed = False
    if survey_data.closed_at or not survey_data.is_active:
        is_closed = True
    elif survey_data.auto_close_after:
        # Verificar si ha pasado el tiempo de auto-cierre
        close_time = survey_data.created_at + timedelta(hours=survey_data.auto_close_after)
        if datetime.now() > close_time:
            is_closed = True
            # Actualizar el estado en la base de datos
            survey_data.closed_at = close_time
            survey_data.is_active = False
            db.session.commit()
    
    # Determinar si el usuario puede responder
    can_respond = (
        is_authorized and  # Está autorizado
        not existing_response and  # No ha respondido ya
        not is_closed  # La encuesta está activa
    )
    
    # Obtener resultados si la encuesta está cerrada O el usuario ya respondió O es admin
    results = None
    if is_closed or existing_response or current_user.is_admin:
        results = get_survey_results(survey_id)
    
    return render_template('survey/view.html',
                          survey=survey_data,
                          existing_response=existing_response,
                          is_closed=is_closed,
                          can_respond=can_respond,
                          results=results)

@survey.route('/encuestas/<int:survey_id>/responder', methods=['POST'])
@login_required
def respond_to_survey(survey_id):
    """Enviar respuesta a una encuesta"""
    # Obtener la encuesta
    survey_data = Survey.query.get_or_404(survey_id)
    
    # Verificar acceso: admin O usuario autorizado
    is_authorized = current_user.is_admin or current_user in survey_data.authorized_users
    
    if not is_authorized:
        flash('No tienes permiso para responder a esta encuesta', 'danger')
        return redirect(url_for('survey.view_survey', survey_id=survey_id))
    
    # Verificar si la encuesta está activa
    if not survey_data.is_active or survey_data.closed_at:
        flash('Esta encuesta está cerrada', 'warning')
        return redirect(url_for('survey.view_survey', survey_id=survey_id))
    
    # Verificar auto-cierre
    if survey_data.auto_close_after:
        close_time = survey_data.created_at + timedelta(hours=survey_data.auto_close_after)
        if datetime.now() > close_time:
            flash('Esta encuesta se ha cerrado automáticamente', 'warning')
            return redirect(url_for('survey.view_survey', survey_id=survey_id))
    
    # Verificar si el usuario ya respondió
    existing_response = SurveyResponse.query.filter_by(
        survey_id=survey_id,
        user_id=current_user.id
    ).first()
    
    if existing_response:
        flash('Ya has respondido a esta encuesta', 'warning')
        return redirect(url_for('survey.view_survey', survey_id=survey_id))
    
    # Procesar la respuesta
    option_id = request.form.get('option')
    if not option_id:
        flash('Debes seleccionar una opción', 'danger')
        return redirect(url_for('survey.view_survey', survey_id=survey_id))
    
    # Verificar que la opción pertenece a la encuesta
    option = SurveyOption.query.filter_by(id=option_id, survey_id=survey_id).first()
    if not option:
        flash('Opción no válida', 'danger')
        return redirect(url_for('survey.view_survey', survey_id=survey_id))
    
    # Crear la respuesta
    response = SurveyResponse(
        survey_id=survey_id,
        option_id=option.id,
        user_id=current_user.id
    )
    
    db.session.add(response)
    
    try:
        db.session.commit()
        flash('¡Respuesta registrada con éxito!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar respuesta: {str(e)}', 'danger')
    
    return redirect(url_for('survey.view_survey', survey_id=survey_id))

@survey.route('/admin/encuestas')
@login_required
@admin_required
def admin_surveys():
    """Panel de administración de encuestas"""
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    
    # Agregar información de respuestas a cada encuesta
    for survey in surveys:
        survey.response_count = SurveyResponse.query.filter_by(survey_id=survey.id).count()
    
    return render_template('survey/admin.html', surveys=surveys, timedelta=timedelta)

@survey.route('/admin/encuestas/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def create_survey():
    """Crear una nueva encuesta"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        auto_close = request.form.get('auto_close')
        auto_close_hours = request.form.get('auto_close_hours', 2)
        
        if not title:
            flash('El título es obligatorio', 'danger')
            return redirect(url_for('survey.create_survey'))
        
        # Crear la encuesta
        new_survey = Survey(
            title=title,
            description=description,
            created_by=current_user.id,
            auto_close_after=int(auto_close_hours) if auto_close else None
        )
        
        db.session.add(new_survey)
        db.session.flush()  # Para obtener el ID generado
        
        # Procesar opciones
        options = request.form.getlist('options[]')
        if not options or len(options) < 2:
            db.session.rollback()
            flash('Debes agregar al menos dos opciones', 'danger')
            return redirect(url_for('survey.create_survey'))
        
        for i, option_text in enumerate(options):
            if option_text.strip():  # Solo agregar opciones no vacías
                option = SurveyOption(
                    survey_id=new_survey.id,
                    text=option_text.strip(),
                    order=i
                )
                db.session.add(option)
        
        # Procesar usuarios autorizados
        authorized_users = request.form.getlist('authorized_users[]')
        if authorized_users:
            users = User.query.filter(User.id.in_(authorized_users)).all()
            new_survey.authorized_users = users
        
        try:
            db.session.commit()
            flash('Encuesta creada con éxito', 'success')
            return redirect(url_for('survey.admin_surveys'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear encuesta: {str(e)}', 'danger')
    
    # Obtener usuarios para el formulario
    users = User.query.filter_by(is_active_member=True).all()
    
    return render_template('survey/create.html', users=users)

@survey.route('/admin/encuestas/<int:survey_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_survey(survey_id):
    """Editar una encuesta existente"""
    survey_data = Survey.query.get_or_404(survey_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        auto_close = request.form.get('auto_close')
        auto_close_hours = request.form.get('auto_close_hours', 2)
        
        if not title:
            flash('El título es obligatorio', 'danger')
            return redirect(url_for('survey.edit_survey', survey_id=survey_id))
        
        # Actualizar la encuesta
        survey_data.title = title
        survey_data.description = description
        survey_data.auto_close_after = int(auto_close_hours) if auto_close else None
        
        # Procesar opciones existentes
        existing_options = {}
        for option in survey_data.options:
            existing_options[option.id] = option
        
        # Obtener opciones del formulario
        option_ids = request.form.getlist('option_ids[]')
        option_texts = request.form.getlist('options[]')
        
        # Actualizar opciones existentes
        for i, (option_id, option_text) in enumerate(zip(option_ids, option_texts)):
            if option_id and option_id.isdigit():
                # Actualizar opción existente
                option_id = int(option_id)
                if option_id in existing_options:
                    existing_options[option_id].text = option_text.strip()
                    existing_options[option_id].order = i
                    # Eliminar de existing_options para saber cuáles hay que borrar
                    del existing_options[option_id]
            elif option_text.strip():
                # Crear nueva opción
                option = SurveyOption(
                    survey_id=survey_id,
                    text=option_text.strip(),
                    order=i
                )
                db.session.add(option)
        
        # Eliminar opciones que ya no existen (solo si no tienen respuestas)
        for option in existing_options.values():
            has_responses = SurveyResponse.query.filter_by(option_id=option.id).count() > 0
            if not has_responses:
                db.session.delete(option)
        
        # Procesar usuarios autorizados
        authorized_users = request.form.getlist('authorized_users[]')
        users = User.query.filter(User.id.in_(authorized_users)).all() if authorized_users else []
        survey_data.authorized_users = users
        
        try:
            db.session.commit()
            flash('Encuesta actualizada con éxito', 'success')
            return redirect(url_for('survey.admin_surveys'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar encuesta: {str(e)}', 'danger')
    
    # Obtener usuarios para el formulario
    users = User.query.filter_by(is_active_member=True).all()
    
    # Obtener IDs de usuarios autorizados
    authorized_user_ids = [user.id for user in survey_data.authorized_users]
    
    return render_template('survey/edit.html', 
                          survey=survey_data,
                          users=users,
                          authorized_user_ids=authorized_user_ids,
                          timedelta=timedelta)

@survey.route('/admin/encuestas/<int:survey_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_survey(survey_id):
    """Activar/desactivar una encuesta"""
    survey_data = Survey.query.get_or_404(survey_id)
    
    action = request.form.get('action')
    
    if action == 'close':
        survey_data.is_active = False
        survey_data.closed_at = datetime.now()
        message = 'Encuesta cerrada con éxito'
    elif action == 'reopen':
        survey_data.is_active = True
        survey_data.closed_at = None
        message = 'Encuesta reabierta con éxito'
    else:
        flash('Acción no válida', 'danger')
        return redirect(url_for('survey.admin_surveys'))
    
    try:
        db.session.commit()
        flash(message, 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('survey.admin_surveys'))

@survey.route('/admin/encuestas/<int:survey_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def delete_survey(survey_id):
    """Eliminar una encuesta"""
    survey_data = Survey.query.get_or_404(survey_id)
    
    try:
        db.session.delete(survey_data)
        db.session.commit()
        flash('Encuesta eliminada con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar encuesta: {str(e)}', 'danger')
    
    return redirect(url_for('survey.admin_surveys'))

@survey.route('/api/encuestas/<int:survey_id>/resultados')
@login_required
def api_survey_results(survey_id):
    """API para obtener resultados de una encuesta en tiempo real"""
    # Verificar si el usuario tiene acceso a la encuesta
    survey_data = Survey.query.get_or_404(survey_id)
    
    # Verificar acceso: admin O usuario autorizado
    is_authorized = current_user.is_admin or current_user in survey_data.authorized_users
    
    if not is_authorized:
        return jsonify({
            'success': False,
            'error': 'No tienes permiso para ver estos resultados'
        }), 403
    
    # Obtener resultados
    results = get_survey_results(survey_id)
    
    return jsonify({
        'success': True,
        'results': results
    })

def get_survey_results(survey_id):
    """Obtiene los resultados REALES de una encuesta (sin votos fantasma)"""
    # Obtener todas las opciones de la encuesta
    options = SurveyOption.query.filter_by(survey_id=survey_id).order_by(SurveyOption.order).all()
    
    # Obtener SOLO respuestas reales de usuarios autenticados
    responses = SurveyResponse.query.filter_by(survey_id=survey_id).all()
    
    # Verificar que las respuestas corresponden a usuarios reales
    valid_responses = []
    for response in responses:
        if response.user_id and User.query.get(response.user_id):
            valid_responses.append(response)
    
    # Contar respuestas por opción
    option_counts = {}
    for option in options:
        option_counts[option.id] = 0
    
    # Contar SOLO respuestas válidas
    for response in valid_responses:
        if response.option_id in option_counts:
            option_counts[response.option_id] += 1
    
    # Calcular porcentajes
    total_responses = len(valid_responses)
    results = []
    
    for option in options:
        count = option_counts[option.id]
        percentage = (count / total_responses * 100) if total_responses > 0 else 0
        
        results.append({
            'id': option.id,
            'text': option.text,
            'count': count,
            'percentage': round(percentage, 1)
        })
    
    return {
        'total': total_responses,
        'options': results
    }