# Python Quest

Python Quest is an interactive Snakes and Ladders learning game built with Flask. Players answer Python MCQs, roll a 3D dice, climb ladders, avoid snakes, and race to square 100.

## Features

- Classic Snakes and Ladders board gameplay
- Custom board image using `snakes-ladders-board.jpg`
- Human vs AI mode
- Local multiplayer mode with 2 to 4 players
- 3D dice roll animation with dot faces
- Python MCQ questions by difficulty
- 400 MCQs for each difficulty:
  - Beginner
  - Intermediate
  - Advanced
- Correct and incorrect answer feedback
- Correct answer is shown after a wrong choice
- Light and dark themes
- Animated snakes and ladders backgrounds on home/setup pages
- Render-ready deployment files

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- HTML
- CSS
- JavaScript
- Bootstrap
- Gunicorn for production hosting

## Project Structure

```text
codex_PythonQuest/
├── app.py
├── config.py
├── generate_questions.py
├── requirements.txt
├── .python-version
├── .gitignore
├── Procfile
├── render.yaml
├── python_quest.db
├── snakes-ladders-board.jpg
├── engine/
│   └── snake_ladder.py
├── models/
│   ├── game.py
│   ├── models.py
│   └── player.py
├── questions/
│   ├── beginner.json
│   ├── intermediate.json
│   └── advanced.json
├── routes/
│   ├── game.py
│   └── home.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── snakes-ladders-board.jpg
│   └── js/
│       └── game.js
└── templates/
    ├── index.html
    ├── setup.html
    └── game.html
```

## Local Setup

### 1. Install Python

Install Python 3.10 or newer from:

```text
https://www.python.org/downloads/
```

During installation, enable:

```text
Add Python to PATH
```

### 2. Open The Project Folder

Open PowerShell or terminal inside the project folder:

```powershell
cd "C:\Users\thira\OneDrive\Desktop\AKASH MINI PROJECT\codex_PythonQuest"
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

If `pip` does not work, try:

```powershell
py -m pip install -r requirements.txt
```

### 4. Run The App

```powershell
python app.py
```

or:

```powershell
py app.py
```

Open the app in your browser:

```text
http://127.0.0.1:5000
```

## Running On Another Device In Same Wi-Fi

Start the app on your computer:

```powershell
python app.py
```

The terminal will show a link like:

```text
Other devices on same Wi-Fi: http://192.168.x.x:5000
```

Open that URL on another phone, laptop, or tablet connected to the same Wi-Fi.

If it does not open, allow Python through Windows Firewall or allow inbound TCP port `5000`.

## Game Modes

### Human vs AI

One player competes against the computer. The AI has different accuracy based on difficulty.

### Local Multiplayer

Choose multiplayer from the setup page, then select:

- 2 Players
- 3 Players
- 4 Players

Players take turns on the same device.

## Question Banks

Questions are stored as JSON files:

```text
questions/beginner.json
questions/intermediate.json
questions/advanced.json
```

Each file contains 400 MCQs.

To regenerate the question banks:

```powershell
python generate_questions.py
```

or:

```powershell
py generate_questions.py
```

## Deploying To Render

This project already includes Render deployment files:

- `requirements.txt`
- `.python-version`
- `Procfile`
- `render.yaml`

### Before Pushing To GitHub

Make sure these files and folders are included:

```text
app.py
config.py
requirements.txt
.python-version
Procfile
render.yaml
engine/
models/
questions/
static/
templates/
```

Do not upload temporary/cache folders. They are already listed in `.gitignore`:

```text
__pycache__/
.codex_deps/
.codex_runtime_deps/
.venv/
venv/
```

### Render Settings

Use these values if Render asks manually:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Deployment Steps

1. Push this project to GitHub.
2. Go to Render:

```text
https://render.com
```

3. Click `New +`.
4. Select `Web Service`.
5. Connect your GitHub repository.
6. Select this project.
7. Use Python as the runtime.
8. Set the build command:

```text
pip install -r requirements.txt
```

9. Set the start command:

```text
gunicorn app:app
```

10. Deploy the service.

After deployment, Render will give a public URL like:

```text
https://python-quest.onrender.com
```

## Environment Variables

For production, set:

```text
SECRET_KEY=your-secret-key
```

If using `render.yaml`, Render can generate this automatically.

## Python Version

The project includes:

```text
.python-version
```

Render uses this file to choose the Python version for deployment. This project is pinned to Python `3.12`.

## Important Notes

- Do not use `python app.py` as the Render start command.
- Use `gunicorn app:app` on Render.
- Keep `.python-version` in the project root.
- Keep `.gitignore` so temporary local folders are not pushed.
- Keep the `questions/` folder uploaded, because the game loads MCQs from JSON files.
- Keep `static/images/snakes-ladders-board.jpg`, because the board uses this image.
- SQLite is included for local use. On free hosting, database file changes may not be permanent, but the game questions are stored in JSON files and will still work.

## Main Pages

```text
/        Home page
/setup   Game settings
/game    Game board
```

## Author

Python Quest was created as a mini project for learning Python through an interactive board game.
