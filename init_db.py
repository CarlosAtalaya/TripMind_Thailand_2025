#!/usr/bin/env python
"""
Script de inicialización de la base de datos
Ejecutar este script para crear la base de datos y las tablas necesarias
"""

from app import app, db, create_tables
from models import User
from votes import initialize_categories

def init_database():
    """Inicializar la base de datos con la estructura necesaria"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✓ Tablas de la base de datos creadas.")
        
        # Inicializar categorías de votación
        initialize_categories()
        print("✓ Categorías de votación inicializadas.")
        
        # Verificar si hay usuarios
        user_count = User.query.count()
        if user_count == 0:
            print("\n⚠️  No hay usuarios en la base de datos.")
            print("La primera vez que accedas a la aplicación, se mostrará")
            print("una página de configuración para crear el usuario administrador.")
        else:
            print(f"\n✓ Base de datos lista con {user_count} usuario(s).")

if __name__ == '__main__':
    print("Inicializando base de datos para TravelBoard...")
    init_database()
    print("\n¡Base de datos inicializada correctamente!")
    print("Puedes iniciar la aplicación con: python app.py")