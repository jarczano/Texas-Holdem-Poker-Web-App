from flask_socketio import emit, join_room, leave_room
from flask import render_template, redirect, url_for, request

from utils import get_ipv4_address
#from poker_game import game
from game_class import Game
from setting import socketio, app, games


@socketio.on('connect')
def on_connect():
    #website_address = request.headers.get('Host')
    #print('website_address', website_address)
    player_id = request.sid
    print('Server. player id: ', player_id)
    if player_id not in games:
        join_room(player_id)
        games[player_id] = Game(player_id)
    #print('numbers of games', len(games))

@app.route('/')
def menu():
    # return render_template('menu.html')
    return render_template('start.html')

# test
@app.route('/menu.html')
def tmenu():
    return render_template('menu.html')

@app.route('/play/<selectedOpponent>')
def render_game(selectedOpponent):
    print("selected opponent server ", selectedOpponent)
    return render_template('game.html')


@socketio.on('start_game')
def start_game():
    print('start game')
    player_id = request.sid
    game = games.get(player_id)
    game.start_game()

    #emit('redirect', {'url': '/'}, broadcast=True)


@socketio.on('player_decision')
def player_decision(player_decision):
    print('player decision from server')
    player_id = request.sid
    game = games.get(player_id)
    game.send_player_decision(player_decision)
    if game.state == 'end':
        print("end from main3")
        emit('redirect', {'url': '/menu.html'}, broadcast=True)


@socketio.on('select_opponent')
def select_opponent(selected_opponent):
    print('selected_opponent', selected_opponent)
    player_id = request.sid
    game = games[player_id]
    #game.opponent = selected_opponent
    print('player id from server',game.player_id)
    game.select_opponent(selected_opponent)


@socketio.on('disconnect')
def on_disconnect():
    player_id = request.sid
    games.pop(player_id, None)



@socketio.on('transfer_socket')
def transfer_socker(socket):
    print('socket', socket)



ip_address = get_ipv4_address()


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host=ip_address, port=5000,
                 ssl_context=('cert.crt', 'private.key'))
'''

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80,  allow_unsafe_werkzeug=True)
'''