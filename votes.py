# votes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, VoteCategory, Vote, User
from datetime import datetime, timedelta
import yaml
import os
import pytz
from config import VOTE_CATEGORIES

votes = Blueprint('votes', __name__)

def get_travelers_from_itinerary(itinerary_name='thailand_2025.yaml'):
    """Obtener la lista de viajeros del itinerario"""
    try:
        file_path = os.path.join('data', 'itineraries', itinerary_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            itinerary = yaml.safe_load(file)
            
        return itinerary.get('travelers', [])
    except Exception as e:
        print(f"Error al obtener viajeros: {e}")
        return []

def get_active_travelers(itinerary_travelers):
    """
    Filtra la lista de viajeros del itinerario para devolver solo los usuarios activos
    
    Args:
        itinerary_travelers: Lista de viajeros del itinerario YAML
        
    Returns:
        list: Lista filtrada de viajeros que son usuarios activos
    """
    # Obtener todos los usuarios activos
    active_users = User.query.filter_by(is_active_member=True).all()
    
    # Mapear usuarios por nombre
    active_users_map = {}
    for user in active_users:
        active_users_map[user.username] = user
        # También consideramos el campo name del usuario
        active_users_map[user.name] = user
    
    # Filtrar viajeros del itinerario que coincidan con usuarios activos
    active_travelers = []
    for traveler in itinerary_travelers:
        traveler_name = traveler['name']
        if traveler_name in active_users_map:
            # Añadir el viajero junto con el usuario relacionado
            active_travelers.append({
                'name': traveler_name,
                'phone': traveler.get('phone', ''),
                'user': active_users_map[traveler_name]
            })
    
    return active_travelers

def get_active_travelers_for_voting():
    """Obtener viajeros activos para votaciones"""
    itinerary_travelers = get_travelers_from_itinerary()
    return get_active_travelers(itinerary_travelers)

def get_daily_mvp():
    """
    Obtiene el ganador de la categoría 'MVP diario' para el día de hoy
    
    Returns:
        dict: Información del ganador o None si no hay ganador
    """
    # Usar el timezone de Tailandia para consistencia con el resto de la aplicación
    thailand_tz = pytz.timezone('Asia/Bangkok')
    today = datetime.now(thailand_tz).date()
    
    # Obtener la categoría MVP diario
    mvp_category = VoteCategory.query.filter_by(name="MVP diario").first()
    if not mvp_category:
        return None
    
    # Obtener todos los votos de hoy para esta categoría
    votes = Vote.query.filter(
        Vote.category_id == mvp_category.id,
        Vote.date == today
    ).all()
    
    if not votes:
        return None
    
    # Contar votos por viajero
    traveler_votes = {}
    for vote in votes:
        if vote.traveler_name not in traveler_votes:
            traveler_votes[vote.traveler_name] = 0
        traveler_votes[vote.traveler_name] += 1
    
    # Si no hay votos contabilizados, devolver None
    if not traveler_votes:
        return None
    
    # En caso de empate, elegimos aleatoriamente entre los que tengan más votos
    max_votes = max(traveler_votes.values())
    winners = [name for name, vote_count in traveler_votes.items() if vote_count == max_votes]
    
    # Elegir al ganador (aleatoriamente en caso de empate)
    import random
    winner_name = random.choice(winners)
    
    # Obtener información adicional del usuario ganador
    winner_user = User.query.filter(
        (User.username == winner_name) | (User.name == winner_name)
    ).first()
    
    return {
        'name': winner_name,
        'votes': traveler_votes[winner_name],
        'user': winner_user,
        'total_voters': len(votes)
    }

def initialize_categories():
    """Inicializar las categorías de votación"""
    for cat in VOTE_CATEGORIES:
        existing = VoteCategory.query.filter_by(name=cat["name"]).first()
        if not existing:
            new_category = VoteCategory(name=cat["name"], description=cat["description"])
            db.session.add(new_category)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error al inicializar categorías: {e}")

@votes.before_request
def before_request():
    """Inicializar categorías antes de cualquier solicitud"""
    initialize_categories()

@votes.route('/votaciones')
@login_required
def index():
    """Página principal de votaciones"""
    categories = VoteCategory.query.all()
    travelers = get_active_travelers_for_voting()
    today = datetime.now().date()
    
    # Obtener votos del usuario actual para hoy
    user_votes_today = Vote.query.filter_by(
        voter_id=current_user.id,
        date=today
    ).all()
    
    # Determinar categorías ya votadas hoy
    voted_categories = [vote.category_id for vote in user_votes_today]
    
    return render_template('votes/index.html', 
                          categories=categories,
                          travelers=travelers,
                          voted_categories=voted_categories)

@votes.route('/votaciones/<int:category_id>', methods=['GET', 'POST'])
@login_required
def vote_category(category_id):
    """Página para votar en una categoría específica"""
    category = VoteCategory.query.get_or_404(category_id)
    
    # Si es la categoría de "Foto del día", redirigir a la página especial
    if category.name == "Foto del día":
        return redirect(url_for('votes.vote_photo_of_day'))
    
    # Obtener solo viajeros activos
    travelers = get_active_travelers_for_voting()
    today = datetime.now().date()
    
    # Verificar si el usuario ya votó en esta categoría hoy
    existing_votes = Vote.query.filter_by(
        category_id=category_id,
        voter_id=current_user.id,
        date=today
    ).all()
    
    if request.method == 'POST':
        if existing_votes:
            flash('Ya has votado en esta categoría hoy', 'warning')
            return redirect(url_for('votes.index'))
        
        # Procesar el voto
        traveler_name = request.form.get('traveler')
        if traveler_name:
            vote = Vote(
                category_id=category_id,
                voter_id=current_user.id,
                traveler_name=traveler_name,
                position=1,  # Siempre posición 1 ya que solo hay un voto
                date=today
            )
            db.session.add(vote)
        
        try:
            db.session.commit()
            flash('¡Voto registrado con éxito!', 'success')
            return redirect(url_for('votes.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar voto: {e}', 'danger')
    
    return render_template('votes/vote_form.html',
                          category=category,
                          travelers=travelers,
                          existing_votes=existing_votes)

@votes.route('/votaciones/foto-del-dia', methods=['GET', 'POST'])
@login_required
def vote_photo_of_day():
    """Página especial para votar en la categoría Foto del día"""
    from daily_photos import get_all_daily_photos
    
    # Obtener la categoría de "Foto del día"
    category = VoteCategory.query.filter_by(name="Foto del día").first()
    if not category:
        flash('Categoría no encontrada', 'danger')
        return redirect(url_for('votes.index'))
    
    today = datetime.now(pytz.timezone('Asia/Bangkok')).date()
    
    # Verificar si el usuario ya votó en esta categoría hoy
    existing_votes = Vote.query.filter_by(
        category_id=category.id,
        voter_id=current_user.id,
        date=today
    ).all()
    
    if request.method == 'POST':
        if existing_votes:
            flash('Ya has votado en esta categoría hoy', 'warning')
            return redirect(url_for('votes.index'))
        
        # Procesar el voto
        traveler_name = request.form.get('traveler')
        if traveler_name:
            vote = Vote(
                category_id=category.id,
                voter_id=current_user.id,
                traveler_name=traveler_name,
                position=1,
                date=today
            )
            db.session.add(vote)
            
            try:
                db.session.commit()
                flash('¡Voto registrado con éxito!', 'success')
                return redirect(url_for('votes.index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error al registrar voto: {e}', 'danger')
    
    # Obtener las fotos del día
    photos = get_all_daily_photos()
    
    return render_template('votes/vote_photo_of_day.html',
                          category=category,
                          photos=photos,
                          existing_votes=existing_votes)

@votes.route('/api/rankings')
def get_rankings():
    """API para obtener los rankings actuales"""
    categories = VoteCategory.query.all()
    travelers = get_travelers_from_itinerary()
    traveler_names = [t['name'] for t in travelers]
    
    # Obtener el período solicitado
    period = request.args.get('period', 'today')
    
    if period == 'today':
        # Solo votos de hoy
        start_date = datetime.now().date()
    else:  # 'all' o cualquier otro valor
        # Todos los votos
        start_date = datetime(1900, 1, 1).date()
    
    rankings = {}
    
    for category in categories:
        # Obtener todos los votos para esta categoría en el período
        votes = Vote.query.filter(
            Vote.category_id == category.id,
            Vote.date >= start_date
        ).all()
        
        # Calcular votos por viajero (ahora es simplemente contar votos)
        traveler_votes = {name: 0 for name in traveler_names}
        for vote in votes:
            if vote.traveler_name in traveler_votes:
                traveler_votes[vote.traveler_name] += 1
        
        # Ordenar por cantidad de votos
        sorted_travelers = sorted(
            traveler_votes.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Guardar el ranking
        rankings[category.name] = [
            {"name": name, "points": votes}
            for name, votes in sorted_travelers
        ]
    
    return jsonify(rankings)

@votes.route('/api/reset_category/<int:category_id>', methods=['POST'])
@login_required
def reset_category(category_id):
    """Resetea todos los votos de una categoría específica (solo admin)"""
    # Verificar que el usuario es administrador
    if not current_user.is_admin:
        return jsonify({
            'success': False,
            'error': 'Solo los administradores pueden resetear las votaciones'
        }), 403
    
    # Verificar que la categoría existe
    category = VoteCategory.query.get(category_id)
    if not category:
        return jsonify({
            'success': False,
            'error': 'Categoría no encontrada'
        }), 404
    
    try:
        # Eliminar todos los votos de esta categoría
        Vote.query.filter_by(category_id=category_id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Todos los votos de la categoría "{category.name}" han sido reseteados'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@votes.route('/api/reset_all_votes', methods=['POST'])
@login_required
def reset_all_votes():
    """Resetea TODOS los votos de TODAS las categorías (solo admin)"""
    # Verificar que el usuario es administrador
    if not current_user.is_admin:
        return jsonify({
            'success': False,
            'error': 'Solo los administradores pueden resetear las votaciones'
        }), 403
    
    try:
        # Eliminar TODOS los votos
        Vote.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Todos los votos de todas las categorías han sido reseteados'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@votes.route('/api/categories')
@login_required
def get_categories():
    """API para obtener todas las categorías con sus IDs"""
    if not current_user.is_admin:
        return jsonify({'error': 'No autorizado'}), 403
    
    categories = VoteCategory.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description
    } for cat in categories])

@votes.route('/votaciones/resultados')
@login_required
def results():
    """Página para ver los resultados de las votaciones"""
    categories = VoteCategory.query.all()
    return render_template('votes/results.html', categories=categories)