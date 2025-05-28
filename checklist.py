# checklist.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, ChecklistItem
from datetime import datetime

checklist = Blueprint('checklist', __name__)

# Elementos del checklist organizados por categorías
CHECKLIST_ITEMS = {
    'documentos': {
        'name': 'Documentación',
        'icon': 'fas fa-passport',
        'color': 'danger',
        'items': {
            'pasaporte': 'Pasaporte (válido mín. 6 meses)',
            'visa': 'Visado para Tailandia (si necesario)',
            'seguro_viaje': 'Seguro de viaje',
            'tarjetas': 'Tarjetas de crédito/débito',
            'efectivo': 'Efectivo (euros para cambiar)',
            'fotocopias': 'Fotocopias de documentos',
            'tarjeta_embarque': 'Tarjetas de embarque (móvil)',
            'reservas_hoteles': 'Confirmaciones de hoteles',
            'itinerario': 'Itinerario impreso/digital'
        }
    },
    'ropa': {
        'name': 'Ropa y Calzado',
        'icon': 'fas fa-tshirt',
        'color': 'primary',
        'items': {
            'camisetas_ligeras': 'Camisetas de manga corta (5-7)',
            'pantalones_cortos': 'Pantalones cortos (3-4)',
            'pantalones_largos': 'Pantalones largos (2-3) - templos',
            'vestidos': 'Vestidos/faldas largas - templos',
            'ropa_interior': 'Ropa interior (7-10 mudas)',
            'calcetines': 'Calcetines (7-10 pares)',
            'pijama': 'Pijama/ropa de dormir',
            'chanclas': 'Chanclas para la ducha',
            'zapatillas_comodas': 'Zapatillas cómodas para caminar',
            'sandalias': 'Sandalias',
            'ropa_lluvia': 'Chubasquero/poncho',
            'bañador': 'Bañador/bikini (2)',
            'gorra': 'Gorra/sombrero'
        }
    },
    'higiene': {
        'name': 'Higiene y Cuidado',
        'icon': 'fas fa-pump-soap',
        'color': 'info',
        'items': {
            'cepillo_dientes': 'Cepillo de dientes',
            'pasta_dientes': 'Pasta de dientes',
            'jabon': 'Jabón/gel de ducha',
            'champu': 'Champú',
            'desodorante': 'Desodorante',
            'protector_solar': 'Protector solar (SPF 50+)',
            'after_sun': 'After sun/aloe vera',
            'repelente': 'Repelente de mosquitos (DEET)',
            'toallas': 'Toallas de microfibra',
            'productos_femeninos': 'Productos de higiene femenina',
            'afeitado': 'Kit de afeitado',
            'perfume': 'Perfume/colonia'
        }
    },
    'botiquin': {
        'name': 'Botiquín y Salud',
        'icon': 'fas fa-first-aid',
        'color': 'success',
        'items': {
            'paracetamol': 'Paracetamol/ibuprofeno',
            'antidiarreicos': 'Antidiarreicos (Fortasec)',
            'probioticos': 'Probióticos',
            'antihistaminicos': 'Antihistamínicos (picaduras)',
            'antiseptico': 'Antiséptico/alcohol',
            'tiritas': 'Tiritas/vendas',
            'termometro': 'Termómetro',
            'medicacion_personal': 'Medicación personal',
            'sales_rehidratacion': 'Sales de rehidratación',
            'vitamina_c': 'Vitamina C',
            'gel_antibacterial': 'Gel antibacterial'
        }
    },
    'tecnologia': {
        'name': 'Tecnología',
        'icon': 'fas fa-mobile-alt',
        'color': 'warning',
        'items': {
            'movil': 'Teléfono móvil',
            'cargador_movil': 'Cargador del móvil',
            'power_bank': 'Power bank/batería externa',
            'cable_usb': 'Cables USB extra',
            'adaptador_corriente': 'Adaptador de corriente universal',
            'camara': 'Cámara de fotos',
            'cargador_camara': 'Cargador de cámara',
            'tarjeta_memoria': 'Tarjetas de memoria extra',
            'auriculares': 'Auriculares',
            'funda_estanca': 'Funda estanca para móvil'
        }
    },
    'viaje': {
        'name': 'Accesorios de Viaje',
        'icon': 'fas fa-suitcase',
        'color': 'secondary',
        'items': {
            'maleta': 'Maleta/mochila principal',
            'equipaje_mano': 'Equipaje de mano',
            'candados': 'Candados para maletas',
            'riñonera': 'Riñonera/bolso pequeño',
            'mochila_dia': 'Mochila para excursiones',
            'almohada_viaje': 'Almohada de viaje',
            'antifaz': 'Antifaz para dormir',
            'tapones_oidos': 'Tapones para los oídos',
            'bolsas_plastico': 'Bolsas de plástico/zip',
            'organizadores': 'Organizadores de equipaje'
        }
    },
    'otros': {
        'name': 'Otros Esenciales',
        'icon': 'fas fa-plus-circle',
        'color': 'dark',
        'items': {
            'agua_botella': 'Botella de agua reutilizable',
            'snacks': 'Snacks para el vuelo',
            'libro_guia': 'Guía de viaje',
            'cuaderno': 'Cuaderno y bolígrafo',
            'gafas_sol': 'Gafas de sol',
            'linterna': 'Linterna pequeña/frontal',
            'navaja_suiza': 'Navaja suiza (en maleta facturada)',
            'papel_higienico': 'Papel higiénico (por si acaso)',
            'toallitas_humedas': 'Toallitas húmedas',
            'dinero_emergencia': 'Dinero de emergencia escondido'
        }
    }
}

@checklist.route('/checklist')
@login_required
def index():
    """Página principal del checklist"""
    # Obtener items marcados por el usuario
    user_items = ChecklistItem.query.filter_by(user_id=current_user.id).all()
    checked_items = {item.item_id: item for item in user_items}
    
    # Calcular estadísticas
    total_items = sum(len(category['items']) for category in CHECKLIST_ITEMS.values())
    checked_count = sum(1 for item in user_items if item.is_checked)
    progress_percentage = (checked_count / total_items * 100) if total_items > 0 else 0
    
    return render_template('checklist/index.html',
                          checklist_items=CHECKLIST_ITEMS,
                          checked_items=checked_items,
                          total_items=total_items,
                          checked_count=checked_count,
                          progress_percentage=progress_percentage)

@checklist.route('/api/checklist/toggle', methods=['POST'])
@login_required
def toggle_item():
    """API para marcar/desmarcar un item del checklist"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({'success': False, 'error': 'Item ID requerido'}), 400
    
    # Buscar el item existente
    checklist_item = ChecklistItem.query.filter_by(
        user_id=current_user.id,
        item_id=item_id
    ).first()
    
    try:
        if checklist_item:
            # Toggle del estado
            checklist_item.is_checked = not checklist_item.is_checked
            checklist_item.checked_at = datetime.now() if checklist_item.is_checked else None
        else:
            # Crear nuevo item marcado
            checklist_item = ChecklistItem(
                user_id=current_user.id,
                item_id=item_id,
                is_checked=True,
                checked_at=datetime.now()
            )
            db.session.add(checklist_item)
        
        db.session.commit()
        
        # Calcular nuevo progreso
        total_items = sum(len(category['items']) for category in CHECKLIST_ITEMS.values())
        user_items = ChecklistItem.query.filter_by(user_id=current_user.id).all()
        checked_count = sum(1 for item in user_items if item.is_checked)
        progress_percentage = (checked_count / total_items * 100) if total_items > 0 else 0
        
        return jsonify({
            'success': True,
            'is_checked': checklist_item.is_checked,
            'checked_count': checked_count,
            'total_items': total_items,
            'progress_percentage': round(progress_percentage, 1)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@checklist.route('/api/checklist/reset', methods=['POST'])
@login_required
def reset_checklist():
    """Resetear todo el checklist del usuario"""
    try:
        ChecklistItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Checklist reseteado correctamente'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500