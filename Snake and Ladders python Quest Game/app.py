from flask import Flask, render_template, request, jsonify
from config import Config
from models.player import db, Player
from engine.snake_ladder import GameEngine
import json
import random
import os
import socket

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Ensure database is created
with app.app_context():
    db.create_all()

# Logic for Snakes and Ladders
SNAKES = {16: 7, 60: 19, 63: 18, 67: 30, 87: 24, 93: 69, 95: 75, 98: 77}
LADDERS = {8: 27, 23: 37, 25: 54, 28: 50, 56: 64, 68: 88, 76: 97, 81: 100}





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    return render_template('setup.html')

@app.route('/game')
def game():
    difficulty = request.args.get('difficulty', 'Beginner')
    mode = request.args.get('mode', 'vs_ai')
    try:
        player_count = int(request.args.get('player_count', 2))
    except ValueError:
        player_count = 2

    player_count = max(2, min(4, player_count))
    if mode != 'multi':
        player_count = 2

    return render_template('game.html', difficulty=difficulty, mode=mode, player_count=player_count)


@app.route('/api/get_question')
def get_question():
    # Use lowercase to match filename 'beginner.json'
    difficulty = request.args.get('difficulty', 'Beginner').lower()
    
    # Define the absolute path to the questions folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(basedir, 'questions', f'{difficulty}.json')
    
    print(f"Looking for question file at: {file_path}") # This helps you debug in the terminal
    
    if not os.path.exists(file_path):
        # Return a sample question if file is missing so the game doesn't break
        return jsonify({
            "topic": "System",
            "question": f"Error: {difficulty}.json not found in questions folder!",
            "options": ["Check Path", "Create File", "Restart Server", "Help"],
            "correctAnswer": "Check Path",
            "explanation": f"Ensure the folder 'questions' exists at {basedir}"
        })

    try:
        with open(file_path, 'r') as f:
            questions = json.load(f)
        return jsonify(random.choice(questions))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ... (keep your existing code) ...

@app.route('/api/move', methods=['POST'])
def move_player():
    data = request.json
    current_pos = data.get('current_pos', 1)
    
    # 1. Roll Dice in Python
    roll = GameEngine.roll_dice()
    
    # 2. Calculate new position
    final_pos, event, intermediate_pos = GameEngine.calculate_move(current_pos, roll)
    
    return jsonify({
        "roll": roll,
        "intermediate_pos": intermediate_pos,
        "final_pos": final_pos,
        "event": event
    })

@app.route('/api/ai_turn')
def ai_turn():
    difficulty = request.args.get('difficulty', 'Beginner')
    # AI accuracy based on requirements
    accuracy_map = {"Beginner": 0.75, "Intermediate": 0.60, "Advanced": 0.45}
    is_correct = random.random() < accuracy_map.get(difficulty, 0.5)
    roll = random.randint(1, 6) if is_correct else 0
    return jsonify({"is_correct": is_correct, "roll": roll})



def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    local_ip = get_local_ip()
    print("\nPython Quest is running:")
    print(f"- This device: http://127.0.0.1:{port}")
    print(f"- Other devices on same Wi-Fi: http://{local_ip}:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
