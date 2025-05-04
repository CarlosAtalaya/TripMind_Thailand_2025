# poop_counter.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, User, PoopCounter
from datetime import datetime

poop_counter = Blueprint('poop_counter', __name__)

@poop_counter.route('/api/poop/increment', methods=['POST'])
@login_required
def increment_counter():
    """Incrementa el contador de cacas del usuario actual"""
    counter = PoopCounter.query.filter_by(user_id=current_user.id).first()
    
    if not counter:
        # Si no existe, crear uno nuevo
        counter = PoopCounter(user_id=current_user.id, count=0)
        db.session.add(counter)
    
    # Incrementar contador
    counter.count += 1
    counter.last_updated = datetime.now()
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'user_id': current_user.id,
            'count': counter.count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@poop_counter.route('/api/poop/counts', methods=['GET'])
@login_required
def get_all_counts():
    """Obtiene los contadores de todos los usuarios"""
    counters = PoopCounter.query.all()
    
    # Crear una lista con todos los contadores
    counts = []
    for counter in counters:
        counts.append({
            'user_id': counter.user_id,
            'user_name': counter.user.name,
            'count': counter.count,
            'last_updated': counter.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # También añadir usuarios que no tienen contador aún
    users_with_counters = [c.user_id for c in counters]
    users_without_counters = User.query.filter(~User.id.in_(users_with_counters)).all()
    
    for user in users_without_counters:
        counts.append({
            'user_id': user.id,
            'user_name': user.name,
            'count': 0,
            'last_updated': None
        })
    
    return jsonify({
        'success': True,
        'counts': counts
    })

@poop_counter.route('/api/poop/reset', methods=['POST'])
@login_required
def reset_all_counters():
    """Resetea todos los contadores de cacas (solo admin)"""
    # Verificar que el usuario es administrador
    if not current_user.is_admin:
        return jsonify({
            'success': False,
            'error': 'Solo los administradores pueden resetear los contadores'
        }), 403
    
    try:
        # Eliminar todos los contadores
        PoopCounter.query.delete()
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Todos los contadores han sido reseteados'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500