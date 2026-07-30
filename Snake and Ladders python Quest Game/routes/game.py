from flask import Blueprint, render_template, request
import json
import random
import os

game_bp = Blueprint('game', __name__)

@game_bp.route('/play')
def play():
    difficulty = request.args.get('difficulty', 'Beginner')
    mode = request.args.get('mode', 'vs_ai')
    return render_template('game.html', difficulty=difficulty, mode=mode)

@game_bp.route('/get_question')
def get_question():
    diff = request.args.get('difficulty', 'Beginner').lower()
    path = f'questions/{diff}.json'
    
    if not os.path.exists(path):
        return {"error": "Question file not found"}, 404
        
    with open(path, 'r') as f:
        questions = json.load(f)
    return random.choice(questions)