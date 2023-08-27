import random

import setting
from player_class import Player
from bot import AI
from deepAI import probability_win
import numpy as np
from setting import BB, show_game
from keras.models import load_model
from flask_socketio import emit
from flask import request
from setting import socketio, games


def auction(player_id, common_cards=None):
    """
    Function made a auction: prepare available options for players, ask players about his decision
    and receive his responses
    :param common_cards: list of common cards, if stage game is preflop then common cards is None
    :return:
    """

    # get live player list
    player_list = Player.player_list
    player_list = [player for player in player_list if player.live]

    number_decisions = sum([player.decision for player in player_list])
    number_player = len(player_list)

    every_fold = False

    # process until every player made decision or every except one fold
    while number_decisions != number_player and not every_fold:

        for player in player_list:

            if not player.decision and player.live:

                # list how much $ players bet in round
                input_stack_list = [player.input_stack for player in player_list]

                # list how much $ players bet in one auction, after each auction attribute bet_auction will be reset
                bet_list = [player.bet_auction for player in player_list]

                # Create a set of options for the player
                dict_options = {'fold': True, 'all-in': True, 'call': False, 'check': False, 'raise': False}

                raise_list = sorted(input_stack_list, reverse=True)
                bet_list = sorted(bet_list, reverse=True)

                # calculate call value, min and max value raise
                call_value = max(input_stack_list) - player.input_stack
                min_raise = call_value + bet_list[0] - bet_list[1]
                if min_raise < BB:
                    min_raise = BB
                max_raise = player.stack

                # activate available option for player
                if player.input_stack == max(input_stack_list):
                    dict_options['check'] = True
                elif player.stack > call_value:
                    dict_options['call'] = True
                if player.stack > min_raise:
                    #dict_options[f'raise: {min_raise}-{max_raise}'] = True
                    dict_options['raise'] = True

                pot = sum(raise_list)  # wszystko co jest do wygrania na stole polozone
                pot_table = sum(input_stack_list) - sum(bet_list)  # to co jest w puli zbudowane przed biezaca licytacja

                # ask player for decision

                if player.kind == 'human':

                    # [option_check, option_call, option_raise_from, option_raise_to]
                    # [True/False, Int/False, Int/False, Int/False]
                    # poprawic call Int or False
                    if dict_options['call']:
                        emit_call_value = call_value
                    else:
                        emit_call_value = False

                    if dict_options['raise']:
                        emit('player_option', [dict_options['check'], emit_call_value, min_raise, max_raise], room=player_id)
                    else:
                        emit('player_option', [dict_options['check'], emit_call_value, False, False], room=player_id)

                    decision = yield 'wait_for_player_decision'


                    print('decision from client', decision)

                elif player.kind == 'bot': # jak tutaj powinny wygladac te nazwy zeby gdzies niezgodnosci nie bylo
                    # this function return choose of AI
                    n_fold = [gamer.live and gamer.alin for gamer in player_list].count(True)
                    n_player_in_round = number_player - n_fold

                    bot = AI(player.cards, dict_options, call_value, min_raise, max_raise, pot, n_player_in_round,
                             common_cards)
                    decision = bot.decision()
                    print('pkt', player.name, decision)

                elif player.kind == 'ai':

                    n_fold = [gamer.live and gamer.alin for gamer in player_list].count(True)
                    n_player_in_round = number_player - n_fold

                    p_win, p_tie = probability_win(player.cards, n_player_in_round, common_cards)

                    if common_cards is None:
                        stage_round = [1, 0, 0, 0]
                    elif len(common_cards) == 3:
                        stage_round = [0, 1, 0, 0]
                    elif len(common_cards) == 4:
                        stage_round = [0, 0, 1, 0]
                    else:
                        stage_round = [0, 0, 0, 1]

                    # prob win, prob tie, pot, if iam starting,stage round [preflop flop turn river]
                    observation = [p_win, p_tie, pot/2000]

                    observation.extend(stage_round)

                    model = load_model('models/model_5001epoch-1688377898.490613.h5')

                    # nie wiem czy jeszcze nie trzeba .reshape(1, 9)
                    best_action_index = np.argmax(model.predict(np.array(observation)))

                    # Needs best action from DNN approximate to best possible action in state

                    # There are 5 possible set of action
                    optimal_bet = best_action_index * 25
                    if optimal_bet > player.stack:
                        optimal_bet = player.stack

                    if dict_options['check'] and dict_options['raise']:
                        #print('set 1')
                        if optimal_bet < abs(optimal_bet - min_raise):
                            decision = ['check']
                        elif min_raise <= optimal_bet <= max_raise:
                            decision = ['raise', optimal_bet]
                        else:
                            decision = ['raise', min_raise]

                    # 2 set
                    elif dict_options['call'] and dict_options['raise']:
                        #print('set 2')
                        if optimal_bet < abs(optimal_bet - call_value):
                            decision = ['fold']
                        elif abs(optimal_bet - call_value) < abs(optimal_bet - min_raise):
                            decision = ['call']
                        elif min_raise <= optimal_bet <= max_raise:
                            decision = ['raise', optimal_bet]
                        else:
                            decision = ['raise', min_raise]

                    # 3 set
                    elif dict_options['call'] and not dict_options['raise']:
                        #print('set 3')
                        if optimal_bet < abs(call_value - optimal_bet):
                            decision = ['fold']
                        elif abs(optimal_bet - player.stack) < abs(optimal_bet - call_value):
                            decision = ['all-in']
                        else:
                            decision = ['call']

                    # 4 set
                    elif dict_options['check'] and not dict_options['raise']:
                        #print('set 4')
                        if optimal_bet < abs(optimal_bet - player.stack):
                            decision = ['check']
                        else:
                            decision = ['all-in']

                    # 5 set
                    elif not dict_options['call'] and not dict_options['check'] and not dict_options['raise']:
                        #print('set 5')
                        if optimal_bet < abs(optimal_bet - player.stack):
                            decision = ['fold']
                        else:
                            decision = ['all-in']

                elif player.kind == 'gpt':
                    # write code for gpt
                    pass




                # Processing of player decision

                if decision[0] == 'raise':
                    chips = int(decision[1])
                    #print(player.name, decision[0], decision[1])
                #else:
                    #print(player.name, decision[0])
                decision = decision[0]

                if show_game:
                    if decision == 'raise':
                        print("{} stack: {} decision: {} {}".format(player.name, player.stack,decision, chips))
                    else:
                        print("{} decision: {}".format(player.name, decision))

                if decision == 'call':
                    chips = max(input_stack_list) - player.input_stack
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()

                elif decision == 'fold':
                    player.fold()

                elif decision == 'check':
                    player.decision = True

                elif decision == 'all-in':
                    player.drop(player.stack)
                    for gamer in player_list:
                        # if any of player bets all-in, then each player who not bet all-in and has bet less than
                        # that player all-in, will have to make the decision again
                        if gamer.live and gamer.decision and gamer.input_stack < player.input_stack:
                            gamer.decision = False
                    player.allin()

                elif decision == 'raise':
                    for gamer in player_list:
                        # a czy tutaj nie musi byc tak jak w przypadku all in ze gracze ktorzy mniej postawili
                        if gamer.live and gamer.decision:
                            gamer.decision = False
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()

                # update info
                emit('update_bet', [player.name, player.bet_auction], room=player_id)
                emit('update_stack', [player.name, player.stack], room=player_id)
                emit('update_pot', [sum([player.input_stack for player in player_list])], room=player_id)

                if player.name != "Alice":
                    if decision == 'raise':
                        emit('opponent_decision', ['Raise', chips], room=player_id)
                    else:
                        emit('opponent_decision', [decision, 0], room=player_id)

                if decision == 'raise':
                    text_decision = 'raise ' + str(chips) + "$" # czy tutaj napenwo jest chips ?
                elif decision == 'call':
                    text_decision = 'call ' + str(chips) + "$"
                elif decision == 'all-in':
                    text_decision = 'all-in for ' + str(player.stack) + "$"
                else:
                    text_decision = decision

                emit('message_decision', player.name + ' ' + text_decision)


            # check if the every except one player fold then don't ask him about decision
            sum_live = 0
            sum_alin = 0
            for gamer in player_list:
                sum_live += gamer.live
                sum_alin += gamer.alin
            if sum_live == 1 and sum_alin == 0:
                every_fold = True
                break
        number_decisions = sum([player.decision for player in player_list])
        #print('\n')

    # After auction players who fold or all-in have no decision made until the next round
    for player in player_list:
        player.next_auction()
        if player.live:
            player.decision = False

