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
    
# Añadir a models.py
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