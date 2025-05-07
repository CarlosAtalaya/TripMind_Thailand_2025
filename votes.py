# votes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, VoteCategory, Vote
from datetime import datetime, timedelta
import yaml
import os

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

def initialize_categories():
    """Inicializar las categorías de votación si no existen"""
    categories = [
        {"name": "MVP diario", "description": "El más valioso del día"},
        {"name": "Donde está Wally", "description": "El que más se pierde"},
        {"name": "Foto del día", "description": "La mejor foto"},
        {"name": "Fue con fé, no con lógica", "description": "Decisiones cuestionables"},
        {"name": "Mamá ven a por mí", "description": "El más desvalido"},
        {"name": "Fashion Victim, Luis Butrón", "description": "El mejor/peor vestido"},
        {"name": "Pa el Tinder", "description": "La foto más seductora"},
        {"name": "El seguro no cubre esto", "description": "La situación más arriesgada"}
    ]
    
    for cat in categories:
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
    travelers = get_travelers_from_itinerary()
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
    travelers = get_travelers_from_itinerary()
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
        
        # Procesar el voto (ahora solo uno)
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

@votes.route('/api/rankings')
def get_rankings():
    """API para obtener los rankings actuales"""
    categories = VoteCategory.query.all()
    travelers = get_travelers_from_itinerary()
    traveler_names = [t['name'] for t in travelers]
    
    # Definir el período para los rankings (últimos 7 días por defecto)
    days = request.args.get('days', 7, type=int)
    if days == 0:  # Si es 0, mostrar de todo el tiempo
        start_date = datetime(1900, 1, 1).date()
    else:
        start_date = datetime.now().date() - timedelta(days=days)
    
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