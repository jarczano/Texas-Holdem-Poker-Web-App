from flask_socketio import emit, join_room, leave_room
from flask import render_template, redirect, url_for, request

from utils import get_ipv4_address
#from poker_game import game
from game_class import Game
from setting import socketio, app, games



#games = {}


@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/play/')
def render_game():
    return render_template('game.html')


@socketio.on('connect')
def on_connect():
    player_id = request.sid
    join_room(player_id)
    game = Game(player_id)
    games[player_id] = game
    #game.start_game()


@socketio.on('start_game')
def start_game(opponent):
    player_id = request.sid
    game = games.get(player_id)
    game.start_game()

    print('end game seer')
    emit('redirect', {'url': '/'}, broadcast=True)


@socketio.on('disconnect')
def on_disconnect():
    player_id = request.sid
    games.pop(player_id, None)




ip_address = get_ipv4_address()


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host=ip_address, port=5000,
                 ssl_context=('cert.crt', 'private.key'))
