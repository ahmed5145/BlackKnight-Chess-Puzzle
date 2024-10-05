const canvas = document.getElementById("chessBoard");
const ctx = canvas.getContext("2d");
const squareSize = 100;

let whitePieces = ['bishop', 'bishop', 'bishop', 'bishop', 'rook', 'knight', 'knight', 'knight', 'knight', 'rook', 'rook', 'rook'];
let whiteLocations = [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [4, 2]];
let blackPieces = ['knight'];
let blackLocations = [[0, 0]]; // Black knight starts at (0, 0)
let selection = -1;
let validMoves = [];
let moveCount = 0; // Track number of moves
let winner = "";

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 6; col++) {
            ctx.fillStyle = (row % 2 === col % 2) ? 'lightgray' : 'white';
            ctx.fillRect(col * squareSize, row * squareSize, squareSize, squareSize);
        }
    }
    ctx.fillStyle = 'gray';
    ctx.fillRect(0, 300, 600, 100);
    ctx.strokeRect(0, 300, 600, 100);
    ctx.fillStyle = 'black';
    ctx.font = "20px Arial";
    ctx.fillText('Black Knight:', 10, 330);
    ctx.fillText('Moves: ' + moveCount, 500, 330);
    ctx.fillText('Get the Black Knight to the bottom right square!', 10, 360);
    ctx.fillText('(CAPTURES NOT ALLOWED, NO COLOR TURNS).', 10, 380);
}

function drawPieces() {
    const images = {
        'bishop': 'assets/images/white bishop.png',
        'rook': 'assets/images/white rook.png',
        'knight': 'assets/images/white knight.png',
        'black_knight': 'assets/images/black knight.png'
    };

    whitePieces.forEach((piece, index) => {
        const img = new Image();
        img.src = images[piece];
        img.onload = () => {
            ctx.drawImage(img, whiteLocations[index][0] * squareSize + 10, whiteLocations[index][1] * squareSize + 10, 80, 80);
        };
    });

    const blackKnightImg = new Image();
    blackKnightImg.src = images['black_knight'];
    blackKnightImg.onload = () => {
        ctx.drawImage(blackKnightImg, blackLocations[0][0] * squareSize + 10, blackLocations[0][1] * squareSize + 10, 80, 80);
    };
}

function highlightMoves(moves) {
    ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
    moves.forEach(move => {
        ctx.fillRect(move[0] * squareSize, move[1] * squareSize, squareSize, squareSize);
    });
}

function isOnBoard(position) {
    return position[0] >= 0 && position[0] < 6 && position[1] >= 0 && position[1] < 3;
}

function checkOptions(piece, location) {
    const movesList = [];
    if (piece === 'knight') {
        const knightMoves = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]];
        knightMoves.forEach(move => {
            const target = [location[0] + move[0], location[1] + move[1]];
            if (isOnBoard(target) && !whiteLocations.some(whiteLoc => whiteLoc[0] === target[0] && whiteLoc[1] === target[1]) &&
                !blackLocations.some(blackLoc => blackLoc[0] === target[0] && blackLoc[1] === target[1])) {
                movesList.push(target);
            }
        });
    }
    return movesList;
}

function checkWhiteOptions(location) {
    const movesList = [];
    const piece = whitePieces.find((_, index) => {
        return whiteLocations[index][0] === location[0] && whiteLocations[index][1] === location[1];
    });
    return checkOptions(piece, location);
}

canvas.addEventListener("click", (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) / squareSize);
    const y = Math.floor((event.clientY - rect.top) / squareSize);

    const clickedLocation = [x, y];

    if (selection === -1) {
        // Check if a white piece was clicked
        const pieceIndex = whiteLocations.findIndex(loc => loc[0] === x && loc[1] === y);
        if (pieceIndex !== -1) {
            selection = pieceIndex; // Select the white piece
            validMoves = checkWhiteOptions(whiteLocations[pieceIndex]);
        } else if (blackLocations[0][0] === x && blackLocations[0][1] === y) {
            selection = 0; // Select black knight
            validMoves = checkOptions(blackPieces[0], blackLocations[0]);
        }
    } else {
        if (validMoves.some(move => move[0] === x && move[1] === y)) {
            if (selection >= 0) {
                // Move white piece
                whiteLocations[selection] = clickedLocation;
                moveCount++;
            } else {
                // Move black knight
                blackLocations[0] = clickedLocation;
                moveCount++;
            }

            // Check win condition
            if (blackLocations[0][0] === 5 && blackLocations[0][1] === 2) {
                winner = `Black Knight wins in ${moveCount} moves!`;
            }
            selection = -1; // Deselect
            validMoves = [];
        } else {
            selection = -1; // Deselect if clicked outside valid moves
            validMoves = [];
        }
    }

    drawGame();
});

function drawGame() {
    drawBoard();
    drawPieces();
    if (validMoves.length > 0) {
        highlightMoves(validMoves);
    }
    if (winner) {
        ctx.fillStyle = 'gold';
        ctx.fillText(winner, 10, 50);
    }
}

drawGame();
