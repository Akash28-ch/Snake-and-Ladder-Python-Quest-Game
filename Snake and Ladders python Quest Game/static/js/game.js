const socket = typeof io === 'function' ? io() : null;
const canvas = document.getElementById('gameBoard');
const ctx = canvas ? canvas.getContext('2d') : null;

let gameState = {
    pos: 1,
    difficulty: new URLSearchParams(window.location.search).get('difficulty') || 'Beginner',
    turnActive: true,
    players: [{ id: 1, pos: 1, name: 'Player 1', color: 'red' }]
};

function showGameMessage(message, type = 'info') {
    const messageElement = document.getElementById('game-message');
    if (messageElement) {
        messageElement.className = `game-message show ${type}`;
        messageElement.innerText = message;
    } else {
        console.log(message);
    }
}

function setDiceRoll(roll) {
    const diceElement = document.getElementById('dice-visual');
    if (!diceElement) return;
    diceElement.dataset.roll = roll;
    diceElement.setAttribute('aria-label', `Dice showing ${roll}`);
}

function drawBoard() {
    if (!ctx) return;

    ctx.clearRect(0, 0, 600, 600);
    const size = 60;
    for (let i = 0; i < 100; i++) {
        const x = (i % 10) * size;
        const y = 540 - Math.floor(i / 10) * size;

        ctx.fillStyle = (Math.floor(i / 10) + i) % 2 === 0 ? '#ecf0f1' : '#bdc3c7';
        ctx.fillRect(x, y, size, size);
        ctx.strokeRect(x, y, size, size);

        ctx.fillStyle = 'black';
        ctx.fillText(i + 1, x + 5, y + 15);
    }

    gameState.players.forEach(player => {
        const coords = getCoords(player.pos);
        ctx.beginPath();
        ctx.arc(coords.x + 30, coords.y + 30, 15, 0, Math.PI * 2);
        ctx.fillStyle = player.color;
        ctx.fill();
    });
}

function getCoords(pos) {
    const index = pos - 1;
    const row = Math.floor(index / 10);
    let col = index % 10;
    if (row % 2 !== 0) col = 9 - col;
    return { x: col * 60, y: 540 - (row * 60) };
}

function fetchQuestion() {
    if (socket) {
        socket.emit('request_question', { difficulty: gameState.difficulty });
    }
}

function submitAnswer(selected, correct, explanation) {
    const isCorrect = selected === correct;
    const expArea = document.getElementById('explanation-area');
    if (expArea) {
        expArea.style.display = 'block';
        expArea.innerHTML = `<p class="${isCorrect ? 'text-success' : 'text-danger'}">${isCorrect ? 'Correct!' : `Wrong. Correct answer: ${correct}`}</p><p>${explanation || ''}</p>`;
    }

    if (isCorrect) {
        document.getElementById('roll-btn').disabled = false;
    } else {
        showGameMessage(`Incorrect. The correct answer is: ${correct}.`, 'danger');
        if (typeof passTurn === 'function') setTimeout(passTurn, 3000);
    }
}

async function handleRoll() {
    const diceElement = document.getElementById('dice-visual');
    const rollBtn = document.getElementById('roll-btn');
    if (!diceElement || !rollBtn) return;

    rollBtn.disabled = true;
    diceElement.classList.add('rolling');

    const response = await fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ current_pos: window.userPos || gameState.pos })
    });
    const result = await response.json();

    setTimeout(() => {
        diceElement.classList.remove('rolling');
        setDiceRoll(result.roll);

        window.userPos = result.intermediate_pos;
        if (typeof moveToken === 'function') moveToken('user-p', window.userPos);

        setTimeout(() => {
            if (result.event === 'snake') {
                showGameMessage('Snake bite! Move down.', 'warning');
            } else if (result.event === 'ladder') {
                showGameMessage('Ladder climb! Move up.', 'success');
            }

            window.userPos = result.final_pos;
            if (typeof moveToken === 'function') moveToken('user-p', window.userPos);
            const userPosition = document.getElementById('user-pos');
            if (userPosition) userPosition.innerText = window.userPos;

            if (window.userPos === 100) {
                celebrateWin();
            } else if (typeof handleAITurn === 'function') {
                handleAITurn();
            }
        }, 800);
    }, 600);
}

function celebrateWin() {
    showGameMessage('PYTHON MASTER! You reached 100!', 'success');
    setTimeout(() => {
        location.href = '/';
    }, 1600);
}

function initBoard() {
    const snakes = [16, 60, 63, 67, 87, 93, 95, 98];
    const ladders = [8, 23, 25, 28, 56, 68, 76, 81];
    const board = document.getElementById('board');
    if (!board) return;

    for (let i = 0; i < 100; i++) {
        const num = i + 1;
        const cell = document.getElementById(`cell-${num}`);
        if (!cell) continue;
        if (snakes.includes(num)) cell.classList.add('snake-head');
        if (ladders.includes(num)) cell.classList.add('ladder-bottom');
        if (num === 100) cell.classList.add('win-cell');
    }
}

if (socket) {
    socket.on('new_question', q => {
        document.getElementById('question-text').innerText = q.question;
        const container = document.getElementById('options-container');
        container.innerHTML = '';
        q.options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'btn btn-outline-primary';
            btn.innerText = opt;
            btn.onclick = () => submitAnswer(opt, q.correctAnswer, q.explanation);
            container.appendChild(btn);
        });
    });

    socket.on('dice_rolled', data => {
        gameState.pos = data.new_pos;
        gameState.players[0].pos = data.new_pos;
        setDiceRoll(data.roll);
        drawBoard();
        if (gameState.pos >= 100) showGameMessage('Winner!', 'success');
        setTimeout(fetchQuestion, 2000);
    });
}

drawBoard();
fetchQuestion();
