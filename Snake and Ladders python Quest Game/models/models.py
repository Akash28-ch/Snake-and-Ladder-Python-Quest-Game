from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Player(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    games_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(20))
    winner_name = db.Column(db.String(80))
    duration_seconds = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScoreRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80))
    score = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    snakes_hit = db.Column(db.Integer)
    ladders_climbed = db.Column(db.Integer)