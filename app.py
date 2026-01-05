from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

WIN_COMBOS = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def check_winner(board):
    for a, b, c in WIN_COMBOS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "draw"
    return None

def minimax(board, is_max, ai, human):
    winner = check_winner(board)
    if winner == ai:
        return 1
    if winner == human:
        return -1
    if winner == "draw":
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = ai
                best = max(best, minimax(board, False, ai, human))
                board[i] = ""
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = human
                best = min(best, minimax(board, True, ai, human))
                board[i] = ""
        return best

def best_move(board, ai, human):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = ai
            score = minimax(board, False, ai, human)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    ai = data["ai"]
    human = data["human"]

    move = best_move(board, ai, human)
    if move is not None:
        board[move] = ai

    winner = check_winner(board)
    return jsonify({"board": board, "winner": winner})

if __name__ == "__main__":
    app.run(debug=True)