# guides.py
from flask import Blueprint, render_template
from flask_login import login_required
from config import (
    DANGEROUS_ANIMALS,
    THAI_FOOD,
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
    """Guía de comida tailandesa"""
    return render_template('guides/thai_food.html', 
                          foods=THAI_FOOD,
                          regional_summary=REGIONAL_SUMMARY)