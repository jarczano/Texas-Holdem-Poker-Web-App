from flask_socketio import SocketIO
from flask import Flask

app = Flask(__name__)
socketio = SocketIO(app)

# blinds
BB = 50
SB = 25

show_game = True
time_pause_round_end = 8





