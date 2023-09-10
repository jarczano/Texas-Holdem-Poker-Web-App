import time

from player_class import Player
from poker_round import poker_round
from split_pot import change_players_positions
from flask_socketio import emit
from setting import time_pause_round_end

def game(opponent, player_id):
    print('game start')
    print('opponent', opponent)
    print('player id from game', player_id)

    player1 = Player('Alice', 1000, 0, 'human')
    # czy tam dalej w kodzie jest cos w zaleznosci od imienia ? chyba tak
    opponent_dict = {'bot': 'Bob', 'ai': 'Carol', 'gpt': "Dave"}
    opponent_name = opponent_dict[opponent]

    player2 = Player(opponent_name, 1000, 1, opponent)

    Player.player_list = [player1, player2]
    Player.player_list_chair = [player1, player2]

    player_list_chair = Player.player_list_chair

    print("number players ", len(player_list_chair))

    end = False
    while not end:

        # Play a round

        yield from poker_round(player_id)

        # Shift the button to the next player
        change_players_positions(shift=1)

        # Reset properties for each player
        [player.next_round() for player in player_list_chair]

        for i in range(len(player_list_chair)):
            if player_list_chair[i].stack == 0:

                for player in player_list_chair:
                    emit('update_stack', [player.name, player.stack], room=player_id)

                winner_index = i ^ 1
                winner_name = player_list_chair[winner_index].name
                end = True
                # now it send name of loser
                emit('finish_game', winner_name + 'win the game', room=player_id)
                time.sleep(time_pause_round_end)
                yield 'end'
        '''
        # Check if players has money
        for player in player_list_chair:
            if player.stack == 0:
                end = True
                # now it send name of loser
                emit('finish_game', [player.name], room=player_id)
                time.sleep(time_pause_round_end)
                yield 'end'
        '''
