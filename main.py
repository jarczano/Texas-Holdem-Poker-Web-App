from flask_socketio import SocketIO, emit
from flask import Flask, render_template, redirect, url_for

from utils import get_ipv4_address
from poker_game import game
from setting import socketio, app


#app = Flask(__name__)
#socketio = SocketIO(app)

@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/play/')
def render_game():
    return render_template('game.html')


@socketio.on('start_game')
def start_game(opponent):
    game(opponent)
    print('end game seer')
    emit('redirect', {'url': '/'}, broadcast=True)


ip_address = get_ipv4_address()


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host=ip_address, port=5000,
                 ssl_context=('cert.crt', 'private.key'))
