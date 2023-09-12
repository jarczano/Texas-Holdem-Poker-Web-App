from flask_socketio import emit, join_room, leave_room
from flask import render_template, request

from app.utils import get_ipv4_address
from app.game_class import Game
from setting import socketio, app, games


@socketio.on('connect')
def on_connect():
    player_id = request.sid

    if player_id not in games:
        join_room(player_id)
        games[player_id] = Game(player_id)


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/menu.html')
def menu():
    return render_template('menu.html')


@app.route('/play/<selectedOpponent>')
def render_game(selectedOpponent):
    return render_template('game.html')


@socketio.on('start_game')
def start_game():
    player_id = request.sid
    game = games.get(player_id)
    game.start_game()


@socketio.on('player_decision')
def player_decision(player_decision):
    player_id = request.sid
    game = games.get(player_id)
    game.send_player_decision(player_decision)
    if game.state == 'end':
        emit('redirect', {'url': '/menu.html'}, broadcast=True)


@socketio.on('select_opponent')
def select_opponent(selected_opponent):
    player_id = request.sid
    game = games[player_id]
    game.select_opponent(selected_opponent)


@socketio.on('disconnect')
def on_disconnect():
    player_id = request.sid
    games.pop(player_id, None)
    leave_room(player_id)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host=get_ipv4_address(), port=5000)
