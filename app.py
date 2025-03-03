from flask import Flask, render_template, request, jsonify, session
from game import TicTacToe
from player import SmartComputerPlayer

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    session['game'] = TicTacToe().__dict__
    session['ai_player'] = SmartComputerPlayer('X').__dict__
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    human_move = int(data['position'])
    
    # Reconstruct objects from session
    game = TicTacToe()
    game.__dict__ = session['game']
    ai_player = SmartComputerPlayer('X')
    ai_player.__dict__ = session['ai_player']
    
    # Process human move
    game.make_move(human_move, 'O')
    
    # Process AI move
    if game.empty_squares() and not game.current_winner:
        ai_move = ai_player.get_move(game)
        game.make_move(ai_move, 'X')
    
    # Save game state
    session['game'] = game.__dict__
    session['ai_player'] = ai_player.__dict__
    
    return jsonify({
        'board': game.board,
        'winner': game.current_winner,
        'game_over': not game.empty_squares()
    })

if __name__ == '__main__':
    app.run(debug=True)