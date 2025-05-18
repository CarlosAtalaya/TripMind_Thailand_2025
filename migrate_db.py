#!/usr/bin/env python
"""
Script para actualizar la base de datos con los nuevos campos
"""

import sqlite3
import os

def migrate_database():
    db_path = 'instance/tripboard.db'
    
    if not os.path.exists(db_path):
        print("Error: No se encuentra la base de datos")
        return
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna is_active_member existe
        cursor.execute("PRAGMA table_info(user)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_active_member' not in columns:
            print("Añadiendo columna is_active_member a la tabla user...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_active_member BOOLEAN DEFAULT 1")
            conn.commit()
            print("✓ Columna is_active_member añadida")
        else:
            print("✓ La columna is_active_member ya existe")
        
        # Verificar si la tabla countdown_event existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='countdown_event'")
        if not cursor.fetchone():
            print("Creando tabla countdown_event...")
            cursor.execute("""
                CREATE TABLE countdown_event (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_datetime DATETIME NOT NULL,
                    is_active BOOLEAN DEFAULT 0,
                    user_to_activate_id INTEGER,
                    message VARCHAR(200) DEFAULT 'UN NUEVO MIEMBRO SE HA UNIDO A LA EXPEDICIÓN!!!',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_to_activate_id) REFERENCES user(id)
                )
            """)
            conn.commit()
            print("✓ Tabla countdown_event creada")
        else:
            print("✓ La tabla countdown_event ya existe")
            
        print("\n¡Migración completada exitosamente!")

        cursor.execute("PRAGMA table_info(countdown_event)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'countdown_type' not in columns:
            print("Añadiendo columna countdown_type a la tabla countdown_event...")
            cursor.execute("ALTER TABLE countdown_event ADD COLUMN countdown_type VARCHAR(20) DEFAULT 'new_member'")
            conn.commit()
            print("✓ Columna countdown_type añadida")
        else:
            print("✓ La columna countdown_type ya existe")
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()