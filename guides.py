# guides.py
from flask import Blueprint, render_template
from flask_login import login_required
from config import (
    DANGEROUS_ANIMALS,
    THAI_MAIN_DISHES,  # Nueva importación
    THAI_DESSERTS,     # Nueva importación  
    THAI_BEVERAGES,    # Nueva importación
    THAI_FOOD,         # Mantener para compatibilidad
    DANGEROUS_PLANTS,
    THAI_TRADITIONS,
    DANGEROUS_PLACES,
    REGIONAL_SUMMARY
)

guides = Blueprint('guides', __name__)


@guides.route('/guias')
@login_required
def index():
    """Página principal de guías"""
    return render_template('guides/index.html')

@guides.route('/guias/animales-peligrosos')
@login_required
def dangerous_animals():
    """Guía de animales peligrosos"""
    return render_template('guides/dangerous_animals.html', 
                          animals=DANGEROUS_ANIMALS,
                          regional_summary=REGIONAL_SUMMARY)

@guides.route('/guias/comida-tailandesa')
@login_required
def thai_food():
    """Guía de comida tailandesa con secciones separadas"""
    return render_template('guides/thai_food.html', 
                          main_dishes=THAI_MAIN_DISHES,
                          desserts=THAI_DESSERTS,
                          beverages=THAI_BEVERAGES,
                          foods=THAI_FOOD,  # Para compatibilidad con código existente
                          regional_summary=REGIONAL_SUMMARY)

@guides.route('/guias/plantas-peligrosas')
@login_required
def dangerous_plants():
    """Guía de plantas peligrosas"""
    return render_template('guides/dangerous_plants.html', 
                          plants=DANGEROUS_PLANTS,
                          regional_summary=REGIONAL_SUMMARY)

@guides.route('/guias/tradiciones-culturales')
@login_required
def thai_traditions():
    """Guía de tradiciones culturales"""
    return render_template('guides/traditions.html', 
                          traditions=THAI_TRADITIONS,
                          regional_summary=REGIONAL_SUMMARY)

@guides.route('/guias/lugares-peligrosos')
@login_required
def dangerous_places():
    """Guía de lugares peligrosos"""
    return render_template('guides/dangerous_places.html', 
                          places=DANGEROUS_PLACES,
                          regional_summary=REGIONAL_SUMMARY)