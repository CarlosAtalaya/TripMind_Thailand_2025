# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active_member = db.Column(db.Boolean, default=True)  # Campo para activación
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
class SharedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.now)
    filesize = db.Column(db.Integer, nullable=False)
    mimetype = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('shared_files', lazy=True))
    
    def __repr__(self):
        return f'<SharedFile {self.original_filename}>'

class VoteCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<VoteCategory {self.name}>'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('vote_category.id'), nullable=False)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    traveler_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)  # 1-5 para la posición
    date = db.Column(db.Date, default=datetime.now().date)
    
    # Relaciones
    category = db.relationship('VoteCategory', backref=db.backref('votes', lazy=True))
    voter = db.relationship('User', backref=db.backref('votes_cast', lazy=True))
    
    def __repr__(self):
        return f'<Vote {self.category.name} - {self.traveler_name} - Pos:{self.position}>'
    
    @property
    def points(self):
        """Calcular puntos basados en la posición"""
        points_map = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
        return points_map.get(self.position, 0)
    
class AppConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    @classmethod
    def get_value(cls, key, default=None):
        """Obtiene el valor de una configuración por su clave"""
        config = cls.query.filter_by(key=key).first()
        return config.value if config else default
    
    @classmethod
    def set_value(cls, key, value, description=None):
        """Establece el valor de una configuración"""
        config = cls.query.filter_by(key=key).first()
        if config:
            config.value = value
            if description:
                config.description = description
        else:
            config = cls(key=key, value=value, description=description)
            db.session.add(config)
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar configuración: {e}")
            return False
    
class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    
    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('diary_entries', lazy=True))
    
    def __repr__(self):
        return f'<DiaryEntry {self.user.name} - {self.date.strftime("%Y-%m-%d")}>'
    
class PoopCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('poop_counter', uselist=False, lazy=True))
    
    def __repr__(self):
        return f'<PoopCounter {self.user.name}: {self.count}>'
    
class CountdownEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_datetime = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    user_to_activate_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    message = db.Column(db.String(200), default="UN NUEVO MIEMBRO SE HA UNIDO A LA EXPEDICIÓN!!!")
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Nuevo campo para indicar el tipo de contador: "new_member" o "custom"
    countdown_type = db.Column(db.String(20), default="new_member")
    
    # Relación con el usuario a activar
    user_to_activate = db.relationship('User', foreign_keys=[user_to_activate_id])

# Many-to-many association table for user permissions
survey_permissions = db.Table('survey_permissions',
    db.Column('survey_id', db.Integer, db.ForeignKey('survey.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    auto_close_after = db.Column(db.Integer, nullable=True)  # Time in hours before auto-close
    
    # Relationships - CORREGIDO: Eliminamos el backref conflictivo
    creator = db.relationship('User', backref=db.backref('created_surveys', lazy=True))
    options = db.relationship('SurveyOption', backref='survey', lazy=True, cascade="all, delete-orphan")
    # CAMBIO: Eliminamos el backref aquí para evitar conflicto
    responses = db.relationship('SurveyResponse', lazy=True, cascade="all, delete-orphan")
    authorized_users = db.relationship('User', secondary='survey_permissions')

class SurveyOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)  # For ordering options

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('survey_option.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships - CORREGIDO: Definimos explícitamente la relación de vuelta
    survey = db.relationship('Survey', back_populates='responses')
    option = db.relationship('SurveyOption')
    user = db.relationship('User')
    
    # Unique constraint to ensure one vote per user per survey
    __table_args__ = (db.UniqueConstraint('survey_id', 'user_id'),)

# IMPORTANTE: Configurar correctamente la relación bidireccional
Survey.responses = db.relationship('SurveyResponse', back_populates='survey', lazy=True, cascade="all, delete-orphan")

class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.String(50), nullable=False)  # ID único del item
    is_checked = db.Column(db.Boolean, default=False)
    checked_at = db.Column(db.DateTime, nullable=True)
    
    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('checklist_items', lazy=True))
    
    # Constraint para evitar duplicados
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id'),)
    
    def __repr__(self):
        return f'<ChecklistItem {self.user.name} - {self.item_id}: {self.is_checked}>'
    
class CustomChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.String(50), nullable=False)  # categoría (documentos, ropa, etc.)
    item_text = db.Column(db.String(200), nullable=False)  # texto del elemento personalizado
    is_checked = db.Column(db.Boolean, default=False)
    checked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relación con el usuario
    user = db.relationship('User', backref=db.backref('custom_checklist_items', lazy=True))
    
    def __repr__(self):
        return f'<CustomChecklistItem {self.user.name} - {self.category_id}: {self.item_text[:30]}...>'