# checklist.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, ChecklistItem, CustomChecklistItem, HiddenChecklistItem
from datetime import datetime
from config import CHECKLIST_ITEMS

checklist = Blueprint('checklist', __name__)

@checklist.route('/checklist')
@login_required
def index():
    """Página principal del checklist"""
    # Obtener items marcados por el usuario (predeterminados)
    user_items = ChecklistItem.query.filter_by(user_id=current_user.id).all()
    checked_items = {item.item_id: item for item in user_items}
    
    # Obtener items personalizados del usuario
    custom_items = CustomChecklistItem.query.filter_by(user_id=current_user.id).all()
    
    # Obtener items ocultos por el usuario
    hidden_items = HiddenChecklistItem.query.filter_by(user_id=current_user.id).all()
    hidden_item_ids = {item.item_id for item in hidden_items}
    
    # Organizar items personalizados por categoría
    custom_items_by_category = {}
    for item in custom_items:
        if item.category_id not in custom_items_by_category:
            custom_items_by_category[item.category_id] = []
        custom_items_by_category[item.category_id].append(item)
    
    # Combinar elementos predeterminados con personalizados para cada categoría
    enhanced_checklist = {}
    for category_id, category_data in CHECKLIST_ITEMS.items():
        enhanced_category = category_data.copy()
        
        # Filtrar elementos predeterminados que NO están ocultos
        filtered_predefined_items = {
            item_id: item_text 
            for item_id, item_text in category_data['items'].items()
            if item_id not in hidden_item_ids
        }
        
        # Empezar con los elementos predeterminados filtrados
        combined_items = filtered_predefined_items.copy()
        
        # Añadir items personalizados
        if category_id in custom_items_by_category:
            for custom_item in custom_items_by_category[category_id]:
                # Usar un ID único para items personalizados
                custom_key = f"custom_{custom_item.id}"
                combined_items[custom_key] = custom_item.item_text
                
                # Añadir el estado de checked para items personalizados
                if custom_item.is_checked:
                    checked_items[custom_key] = custom_item
        
        enhanced_category['items'] = combined_items
        enhanced_category['custom_items'] = custom_items_by_category.get(category_id, [])
        enhanced_checklist[category_id] = enhanced_category
    
    # Calcular estadísticas totales
    total_items = sum(len(category['items']) for category in enhanced_checklist.values())
    
    # Contar items predeterminados marcados
    checked_count = sum(1 for item in user_items if item.is_checked)
    
    # Contar items personalizados marcados
    checked_count += sum(1 for item in custom_items if item.is_checked)
    
    progress_percentage = (checked_count / total_items * 100) if total_items > 0 else 0
    
    return render_template('checklist/index.html',
                          checklist_items=enhanced_checklist,
                          checked_items=checked_items,
                          total_items=total_items,
                          checked_count=checked_count,
                          progress_percentage=progress_percentage)

@checklist.route('/api/checklist/toggle', methods=['POST'])
@login_required
def toggle_item():
    """API para marcar/desmarcar un item del checklist (predeterminado o personalizado)"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({'success': False, 'error': 'Item ID requerido'}), 400
    
    try:
        # Verificar si es un elemento personalizado
        if item_id.startswith('custom_'):
            # Manejar elemento personalizado
            real_id = int(item_id.replace('custom_', ''))
            custom_item = CustomChecklistItem.query.filter_by(
                id=real_id,
                user_id=current_user.id
            ).first()
            
            if not custom_item:
                return jsonify({'success': False, 'error': 'Elemento personalizado no encontrado'}), 404
            
            # Toggle del estado
            custom_item.is_checked = not custom_item.is_checked
            custom_item.checked_at = datetime.now() if custom_item.is_checked else None
            
            db.session.commit()
            
            is_checked = custom_item.is_checked
            
        else:
            # Manejar elemento predeterminado (lógica original)
            checklist_item = ChecklistItem.query.filter_by(
                user_id=current_user.id,
                item_id=item_id
            ).first()
            
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
            is_checked = checklist_item.is_checked
        
        # Calcular nuevo progreso total
        # Items predeterminados
        user_items = ChecklistItem.query.filter_by(user_id=current_user.id).all()
        predefined_checked = sum(1 for item in user_items if item.is_checked)
        
        # Items personalizados
        custom_items = CustomChecklistItem.query.filter_by(user_id=current_user.id).all()
        custom_checked = sum(1 for item in custom_items if item.is_checked)
        
        # Total
        total_predefined = sum(len(category['items']) for category in CHECKLIST_ITEMS.values())
        total_custom = len(custom_items)
        total_items = total_predefined + total_custom
        
        checked_count = predefined_checked + custom_checked
        progress_percentage = (checked_count / total_items * 100) if total_items > 0 else 0
        
        return jsonify({
            'success': True,
            'is_checked': is_checked,
            'checked_count': checked_count,
            'total_items': total_items,
            'progress_percentage': round(progress_percentage, 1)
        })
        
    except ValueError:
        return jsonify({'success': False, 'error': 'ID de elemento no válido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@checklist.route('/api/checklist/reset', methods=['POST'])
@login_required
def reset_checklist():
    """Resetear todo el checklist del usuario (predeterminados, personalizados y ocultos)"""
    try:
        # Eliminar elementos predeterminados marcados
        ChecklistItem.query.filter_by(user_id=current_user.id).delete()
        
        # Eliminar elementos personalizados
        CustomChecklistItem.query.filter_by(user_id=current_user.id).delete()
        
        # Eliminar elementos ocultos (restaurarlos)
        HiddenChecklistItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Checklist reseteado correctamente (incluyendo elementos ocultos restaurados)'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@checklist.route('/api/checklist/add-custom', methods=['POST'])
@login_required
def add_custom_item():
    """Añadir un elemento personalizado a una categoría"""
    data = request.get_json()
    category_id = data.get('category_id')
    item_text = data.get('item_text', '').strip()
    
    if not category_id or not item_text:
        return jsonify({'success': False, 'error': 'Categoría y texto son requeridos'}), 400
    
    if category_id not in CHECKLIST_ITEMS:
        return jsonify({'success': False, 'error': 'Categoría no válida'}), 400
    
    if len(item_text) > 200:
        return jsonify({'success': False, 'error': 'El texto es demasiado largo (máximo 200 caracteres)'}), 400
    
    try:
        # Crear el nuevo elemento personalizado
        custom_item = CustomChecklistItem(
            user_id=current_user.id,
            category_id=category_id,
            item_text=item_text
        )
        
        db.session.add(custom_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Elemento añadido correctamente',
            'item_id': f"custom_{custom_item.id}",
            'item_text': item_text
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@checklist.route('/api/checklist/remove-custom', methods=['POST'])
@login_required
def remove_custom_item():
    """Eliminar un elemento personalizado"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id or not item_id.startswith('custom_'):
        return jsonify({'success': False, 'error': 'ID de elemento no válido'}), 400
    
    try:
        # Extraer el ID real del elemento personalizado
        real_id = int(item_id.replace('custom_', ''))
        
        # Buscar y eliminar el elemento
        custom_item = CustomChecklistItem.query.filter_by(
            id=real_id,
            user_id=current_user.id
        ).first()
        
        if not custom_item:
            return jsonify({'success': False, 'error': 'Elemento no encontrado'}), 404
        
        db.session.delete(custom_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Elemento eliminado correctamente'
        })
        
    except ValueError:
        return jsonify({'success': False, 'error': 'ID de elemento no válido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@checklist.route('/api/checklist/show-default', methods=['POST'])
@login_required
def show_default_item():
    """Mostrar un elemento predeterminado que estaba oculto"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id:
        return jsonify({'success': False, 'error': 'ID de elemento requerido'}), 400
    
    try:
        # Buscar y eliminar el registro de elemento oculto
        hidden_item = HiddenChecklistItem.query.filter_by(
            user_id=current_user.id,
            item_id=item_id
        ).first()
        
        if not hidden_item:
            return jsonify({'success': False, 'error': 'Elemento no encontrado en la lista de ocultos'}), 404
        
        db.session.delete(hidden_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Elemento restaurado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@checklist.route('/api/checklist/hide-default', methods=['POST'])
@login_required
def hide_default_item():
    """Ocultar un elemento predeterminado"""
    data = request.get_json()
    item_id = data.get('item_id')
    
    if not item_id or item_id.startswith('custom_'):
        return jsonify({'success': False, 'error': 'ID de elemento no válido'}), 400
    
    # Verificar que el elemento existe en los elementos predeterminados
    item_exists = False
    for category in CHECKLIST_ITEMS.values():
        if item_id in category['items']:
            item_exists = True
            break
    
    if not item_exists:
        return jsonify({'success': False, 'error': 'Elemento predeterminado no encontrado'}), 400
    
    try:
        # Verificar si ya está oculto
        existing_hidden = HiddenChecklistItem.query.filter_by(
            user_id=current_user.id,
            item_id=item_id
        ).first()
        
        if existing_hidden:
            return jsonify({'success': False, 'error': 'El elemento ya está oculto'}), 400
        
        # Crear el registro de elemento oculto
        hidden_item = HiddenChecklistItem(
            user_id=current_user.id,
            item_id=item_id
        )
        
        db.session.add(hidden_item)
        
        # También eliminar el registro de ChecklistItem si existe (ya que no se puede marcar algo oculto)
        existing_checklist_item = ChecklistItem.query.filter_by(
            user_id=current_user.id,
            item_id=item_id
        ).first()
        
        if existing_checklist_item:
            db.session.delete(existing_checklist_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Elemento ocultado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500