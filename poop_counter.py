# poop_counter.py
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, User, PoopCounter
from datetime import datetime
import yaml
import os

poop_counter = Blueprint('poop_counter', __name__)

def get_traveler_name_mapping():
    """Obtener mapeo entre nombres de usuarios y nombres de viajeros del itinerario"""
    try:
        # Cargar el itinerario para obtener los nombres de viajeros
        file_path = os.path.join('data', 'itineraries', 'thailand_2025.yaml')
        with open(file_path, 'r', encoding='utf-8') as file:
            itinerary = yaml.safe_load(file)
        
        # Crear un diccionario de mapeo basado en los usuarios existentes
        users = User.query.all()
        user_mapping = {}
        
        for user in users:
            # Intentar encontrar el nombre del viajero que coincida con el nombre del usuario
            for traveler in itinerary.get('travelers', []):
                # Comparar el username o name del usuario con el nombre del viajero
                if user.username == traveler['name'] or user.name == traveler['name']:
                    user_mapping[user.id] = traveler['name']
                    break
        
        return user_mapping
    except Exception as e:
        print(f"Error al obtener mapeo de viajeros: {e}")
        return {}

@poop_counter.route('/api/poop/increment', methods=['POST'])
@login_required
def increment_counter():
    """Incrementa el contador de cacas del usuario actual"""
    counter = PoopCounter.query.filter_by(user_id=current_user.id).first()
    
    # Obtener información adicional si está disponible
    data = request.get_json() if request.is_json else {}
    poop_quality = data.get('quality', 'good')  # Por defecto 'good' si no se especifica
    
    if not counter:
        # Si no existe, crear uno nuevo
        counter = PoopCounter(user_id=current_user.id, count=0)
        db.session.add(counter)
    
    # Incrementar contador
    counter.count += 1
    counter.last_updated = datetime.now()
    
    # Opcionalmente, guardar calidad en un registro o log para futuras funcionalidades
    # Esto podría expandirse para rastrear estadísticas por tipo de caca
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'user_id': current_user.id,
            'count': counter.count,
            'quality': poop_quality
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
    """Obtiene los contadores de todos los usuarios activos"""
    # Obtener mapeo de nombres
    traveler_mapping = get_traveler_name_mapping()
    
    # Obtener solo los usuarios activos
    active_users = User.query.filter_by(is_active_member=True).all()
    active_user_ids = [user.id for user in active_users]
    
    # Filtrar solo contadores de usuarios activos
    counters = PoopCounter.query.filter(PoopCounter.user_id.in_(active_user_ids)).all()
    
    # Crear una lista con los contadores de usuarios activos
    counts = []
    for counter in counters:
        # Usar el mapeo para obtener el nombre del viajero
        traveler_name = traveler_mapping.get(counter.user_id, counter.user.name)
        
        counts.append({
            'user_id': counter.user_id,
            'user_name': traveler_name,  # Usar el nombre mapeado
            'count': counter.count,
            'last_updated': counter.last_updated.strftime('%Y-%m-%d %H:%M:%S') if counter.last_updated else None
        })
    
    # También añadir usuarios activos que no tienen contador aún
    users_with_counters = [c.user_id for c in counters]
    active_users_without_counters = [u for u in active_users if u.id not in users_with_counters]
    
    for user in active_users_without_counters:
        # Usar el mapeo para obtener el nombre del viajero
        traveler_name = traveler_mapping.get(user.id, user.name)
        
        counts.append({
            'user_id': user.id,
            'user_name': traveler_name,  # Usar el nombre mapeado
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