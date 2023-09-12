from app.player_class import Player
from setting import show_game
from flask_socketio import emit
import operator


def split_pot(player_id):

    # The split_pot function takes one parameter: list of object players.
    # Function changing attribute stack this object and returns how much they win.

    player_list = Player.player_list_chair.copy()

    # Remove players which fold
    for player in player_list:
        if player.live is False and player.alin is False:
            # nagroda jezeli foldowach
            ''' to jest chyba kawalek od uczenia DNN
            if player.kind == "deepAI":
                #print("split pot action used1", player.action_used)

                player.reward = -player.input_stack
                #yield np.zeros(4) - 1, -player.input_stack, False, player.action_used
            '''
            player_list.remove(player)

    # To calculate reword function needs sorted players list with a descending order and then ascending input stack
    player_list.sort(key=operator.attrgetter('input_stack'))
    player_list.sort(key=operator.attrgetter('score'), reverse=True)
    n = len(player_list)
    player_score, input_stack = [], []

    for player in player_list:
        player_score.append(player.score)
        input_stack.append(player.input_stack)

    win_list = [0] * n
    input_in_game = [0] * n

    # Calculates how many players will be given back the chips they have put into the main pot
    for i in range(n):
        if player_score[i] == max(player_score):
            input_in_game[i] = input_stack[i]
        else:
            aux = [0] * n
            new_input = [0] * n
            for j in range(n):
                if player_score[j] != player_score[i]:
                    aux[j] = 1
            for j in range(n):
                new_input[j] = aux[j] * input_stack[j]
            if input_stack[i] - max(new_input[0:i]) < 0:
                input_in_game[i] = 0
            else:
                input_in_game[i] = input_stack[i] - max(new_input[0:i])

    # Calculates how many each player wins the chips
    for i in range(n):
        number_division = player_score[i:].count(player_score[i])
        for j in range(i + 1, n):
            if player_score[i] > player_score[j]:
                if input_stack[i] >= input_stack[j]:
                    win_list[i] += input_stack[j] / number_division
                    input_stack[j] = 0
                elif input_stack[i] < input_stack[j]:
                    win_list[i] += input_stack[i] / number_division
                    input_stack[j] -= input_stack[i]
        if number_division > 1:
            for k in range(i + 1, n):
                if player_score[i] == player_score[k]:
                    win_list[k] = win_list[i]
                    input_stack[k] -= input_stack[i]

    # Sum of chips returned and won
    emit_content = []
    for i in range(n):
        win_value = input_in_game[i] + win_list[i]
        player_list[i].win(win_value)
        emit_content.extend([player_list[i].name, player_list[i].hand, win_value])

        # emit('finish_round_split_pot', [player_list[i].name, player_list[i].hand, win_value])
        if show_game:
            print(player_list[i].name, " with: ", player_list[i].hand, 'won ', win_value - player_list[i].input_stack)
        #print(player_list[i].name, player_list[i].stack, player_list[i].input_stack)

    # send info about win
    emit('finish_round_split_pot', emit_content, room=player_id)


def one_player_win(player_id):

    #  Function changing player stack who win, and return list tuple who win and how much

    player_list = Player.player_list_chair.copy()
    list_winner = []
    for player in player_list:
        if player.live or player.alin:
            win_value = sum([player.input_stack for player in player_list])
            player.win(win_value)
            list_winner.append((player, win_value - player.input_stack))

            # send info about reward to the client
            emit('finish_round_one_player', [player.name, win_value], room=player_id)

            if show_game:
                print("{} win {}".format(player.name,  win_value - player.input_stack))


def change_players_positions(shift):
    # Function change each player position
    # order in Player.player_list are changed


    player_list = Player.player_list
    number_players = len(player_list)
    for player in player_list:
        player.position = (player.position + shift) % number_players
    player_list.sort(key=operator.attrgetter('position'))

