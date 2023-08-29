import random

from flask_socketio import emit, join_room, leave_room
from flask import render_template, redirect, url_for, request

from utils import get_ipv4_address
#from poker_game import game
#from game_class import Game
from setting import socketio, app, games, players_response


#def one_game(opponent, player_id):
#    game(opponent, player_id)


def test_emit():
    emit('test')


def test_game(start_count, id_player):

    while True:
        #print('emit for test game',start_count)
        #emit('test_game', start_count, room=id_player)
        emit('test_game', start_count)
        socketio.sleep(1)
        start_count += 1


#games = {}
#games_processes = []

@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/play/')
def render_game():
    return render_template('game.html')


@socketio.on('connect')
def on_connect():
    print("server connect")

    player_id = request.sid
    join_room(player_id)

    ra = random.randint(0, 100)
    test_game(ra, player_id)






@socketio.on('start_game')
def start_game(opponent):
    player_id = request.sid
    print('player id from flask', player_id)
    #games[player_id] = Process(target=game, args=(opponent, player_id,))

    #print('end game seer')
    #emit('redirect', {'url': '/'}, broadcast=True)





@socketio.on('player_decision')
def player_decision(player_decision):
    player_id = request.sid
    players_response[player_id] = player_decision
        #global response_decision
        #response_decision = player_decision



@socketio.on('disconnect')
def on_disconnect():
    player_id = request.sid
    games.pop(player_id, None)



ip_address = get_ipv4_address()


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host=ip_address, port=5000,
                 ssl_context=('cert.crt', 'private.key'))
