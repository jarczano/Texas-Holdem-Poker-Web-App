from poker_game import game
from player_class import Player


class Game:
    def __init__(self, player_id):
        self.player_id = player_id
        self.opponent = 'bot' # bot, ai , gpt
        self.game_generator = None
        self.player_decision = None
        self.state = None # 'end' or 'wait_player_decision'

    def start_game(self):
        self.game_generator = game(self.opponent, self.player_id)
        next(self.game_generator)

    def send_player_decision(self, player_response):
        self.player_decision = player_response
        self.state = self.game_generator.send(self.player_decision)

    def select_opponent(self, opponent):
        self.opponent = opponent

    # kiedy otrzemam player_decision od klienta to:
    # do self.player_decision  przypisz ta decyzje
    # odpalac send_player_decision()
    # pozniej sprawdz jeżeli game.state == 'wait':
    #  odpalaj send_player_decision
    # if game_state == 'end'
    # kuniec