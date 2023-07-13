from player_class import Player
from poker_round import poker_round
from split_pot import change_players_positions
from flask_socketio import emit

def game(opponent):
    p1 = Player('Alice', 100, 'human')
    p2 = Player('Bob', 100, opponent)

    player_list_chair = Player.player_list_chair
    print("number players ", len(player_list_chair))

    end = False
    while not end:

        # Play a round

        poker_round()

        # Shift the button to the next player
        change_players_positions(shift=1)

        # Reset properties for each player
        [player.next_round() for player in player_list_chair]

        # Check if players has money
        for player in player_list_chair:
            if player.stack == 0:
                end = True
            else:
                emit('finish_game', [player.name])

        # kill players
        '''
        if end:
            for i in range(len(player_list_chair)):
                del player_list_chair[len(player_list_chair) - i - 1]
                # tutaj by trzeba wysłąc zakonczenie gry
'''
