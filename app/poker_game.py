import time
from flask_socketio import emit

from app.player_class import Player
from app.poker_round import poker_round
from app.split_pot import change_players_positions
from setting import time_pause_round_end


def game(opponent, player_id):
    """
    This function works as generator. Plays a poker match.
    Sends information to the client about situation on the table.
    :param opponent: kind of opponent: bot, ai, gpt
    :param player_id: sid number
    :return: yield 'wait_for_player_decision' when is turn for client. yield 'end' at the end of the game
    """
    opponent_dict = {'bot': 'Bob', 'ai': 'Carol', 'gpt': "Dave"}
    opponent_name = opponent_dict[opponent]

    player1 = Player('Alice', 1000, 0, 'human')
    player2 = Player(opponent_name, 1000, 1, opponent)

    Player.player_list = [player1, player2]
    Player.player_list_chair = [player1, player2]

    player_list_chair = Player.player_list_chair

    end = False
    while not end:

        # Play a round
        yield from poker_round(player_id)

        # Shift the button to the next player
        change_players_positions(shift=1)

        # Reset properties for each player
        [player.next_round() for player in player_list_chair]

        # Checks if anyone has lost
        for i in range(len(player_list_chair)):
            if player_list_chair[i].stack == 0:

                for player in player_list_chair:
                    emit('update_stack', [player.name, player.stack], room=player_id)

                winner_index = i ^ 1
                winner_name = player_list_chair[winner_index].name
                end = True

                emit('finish_game', winner_name + 'win the game', room=player_id)
                time.sleep(time_pause_round_end)
                yield 'end'

