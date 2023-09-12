class Player(object):
    """
    Class for active player
    """
    player_list = []
    player_list_chair = []
    # player_list_chair and player_list is list of all players the difference is that the order in player_list
    # will be change after each round, order of player_list_chair are still this same
    # _position = 0

    def __init__(self, name, stack, position, kind='human'):
        # self.__class__.player_list.append(self)
        # self.__class__.player_list_chair.append(self)
        self.name = name
        self.kind = kind  # human / bot / ai / gpt
        self.stack = stack
        # self.position = Player._position
        self.position = position
        self.live = True
        self.alin = False
        self.cards = ''
        self.score = 0
        self.hand = ''
        self.input_stack = 0  # how much $ player bet in round
        self.bet_auction = 0  # how much $ player bet in one auction, after each auction this attribute will be reset
        self.win_chips = 0
        self.decision = False
        self.action_used = None
        self.reward = 0

        # Player._position += 1

    def allin(self):
        # player will not be asked in the auction
        self.live = False
        self.alin = True
        self.decision = True

    def win(self, chips):
        self.stack += int(chips)
        self.win_chips += chips

    def drop(self, chips):
        self.stack -= int(chips)
        self.input_stack += chips
        self.decision = True
        self.bet_auction += chips

    def blind(self, chips):
        self.stack -= chips
        self.input_stack += chips
        self.bet_auction += chips

    def next_round(self):
        self.live = True
        self.alin = False
        self.cards = ''
        self.score = 0
        self.hand = ''
        self.input_stack = 0
        self.win_chips = 0
        self.decision = False

    def fold(self):
        self.live = False
        self.score = 0
        self.decision = True

    def next_auction(self):
        self.bet_auction = 0

    def next_game(self):
        # self.position = Player._position
        self.live = True
        self.alin = False
        self.cards = ''
        self.score = 0
        self.hand = ''
        self.input_stack = 0  # how much $ player bet in round
        self.bet_auction = 0  # how much $ player bet in one auction, after each auction this attribute will be reset
        self.win_chips = 0
        self.decision = False
        self.stack = 1000
        self.action_used = None

