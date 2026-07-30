from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    games_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)
    
    # Stats for Leaderboard
    total_snakes = db.Column(db.Integer, default=0)
    total_ladders = db.Column(db.Integer, default=0)
    accuracy = db.Column(db.Float, default=0.0)