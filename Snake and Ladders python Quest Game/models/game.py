from .player import db
from datetime import datetime

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(20))
    winner_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)