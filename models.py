from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    plan = db.Column(db.String(20), default='free')  # 'free', 'pro', 'per_export'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    itineraries = db.relationship('Itinerary', backref='user', lazy=True)
    usage_records = db.relationship('UsageRecord', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_remaining_free_uses(self):
        today = datetime.utcnow().date()
        today_uses = UsageRecord.query.filter(
            UsageRecord.user_id == self.id,
            db.func.date(UsageRecord.created_at) == today,
            UsageRecord.plan == 'free'
        ).count()
        return max(0, 3 - today_uses)

class Itinerary(db.Model):
    __tablename__ = 'itineraries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    destinations = db.Column(db.Text)  # JSON string
    travel_dates = db.Column(db.Text)  # JSON string
    traveler_type = db.Column(db.String(50))
    budget = db.Column(db.Float)
    currency = db.Column(db.String(10))
    interests = db.Column(db.Text)
    notes = db.Column(db.Text)
    itinerary_data = db.Column(db.Text)  # JSON string of full itinerary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    plan_used = db.Column(db.String(20))  # Which plan was used to generate
    
    def set_destinations(self, destinations_list):
        self.destinations = json.dumps(destinations_list)
    
    def get_destinations(self):
        return json.loads(self.destinations) if self.destinations else []
    
    def set_travel_dates(self, dates_dict):
        self.travel_dates = json.dumps(dates_dict)
    
    def get_travel_dates(self):
        return json.loads(self.travel_dates) if self.travel_dates else {}
    
    def set_itinerary_data(self, itinerary_dict):
        self.itinerary_data = json.dumps(itinerary_dict)
    
    def get_itinerary_data(self):
        return json.loads(self.itinerary_data) if self.itinerary_data else {}

class UsageRecord(db.Model):
    __tablename__ = 'usage_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan = db.Column(db.String(20))  # 'free', 'pro', 'per_export'
    action = db.Column(db.String(50))  # 'itinerary_generation', 'pdf_export', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)