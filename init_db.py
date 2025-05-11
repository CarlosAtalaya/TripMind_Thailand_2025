#!/usr/bin/env python
"""
Script de inicialización de la base de datos
Ejecutar este script para crear la base de datos y las tablas necesarias
"""

from app import app, db, create_tables
from models import User, CountdownEvent
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

def update_database():
    """Actualizar la estructura de la base de datos"""
    with app.app_context():
        # Esto creará las nuevas tablas sin afectar las existentes
        db.create_all()
        print("✓ Base de datos actualizada.")
        
        # Asegurarse de que las categorías de votación existen
        initialize_categories()
        print("✓ Categorías de votación verificadas.")

if __name__ == '__main__':
    '''
    print("Inicializando base de datos para TravelBoard...")
    init_database()
    print("\n¡Base de datos inicializada correctamente!")
    print("Puedes iniciar la aplicación con: python app.py")
    '''
    print("Actualizando base de datos para TravelBoard...")
    update_database()
    print("\n¡Base de datos actualizada correctamente!")