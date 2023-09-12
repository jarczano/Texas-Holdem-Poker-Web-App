import random
from keras.models import load_model

from app.player_class import Player
from app.bot import AI
from app.deepAI import probability_win
from setting import BB, SB, show_game
from flask_socketio import emit
from app.utils import custom_argmax, get_content


def auction(player_id, common_cards=None):
    """
    Function made a auction: prepare available options for players, ask players about his decision
    and receive his responses
    :param player_id: client sid number
    :param common_cards: list of common cards, if stage game is preflop then common cards is None
    :return:
    """

    # get alive player list
    player_list = Player.player_list
    player_list = [player for player in player_list if player.live]

    number_decisions = sum([player.decision for player in player_list])
    number_player = len(player_list)

    every_fold = False

    # process until every player made decision or every except one fold
    while number_decisions != number_player and not every_fold:

        # ask players about their decision
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
                    dict_options['raise'] = True

                pot = sum(raise_list)  # everything that's on the table
                pot_table = sum(input_stack_list) - sum(bet_list)  # everything that's was in pot before current auction

                # ask player for decision
                # to handle decision is dict_options, min_raise, max_raise and call_value.
                # Additional information is pot, stage

                if player.kind == 'human':

                    # [option_check, option_call, option_raise_from, option_raise_to]
                    #  example: [True/False, Int/False, Int/False, Int/False]
                    if dict_options['call']:
                        emit_call_value = call_value
                    else:
                        emit_call_value = False

                    if dict_options['raise']:
                        emit('player_option', [dict_options['check'], emit_call_value, min_raise, max_raise], room=player_id)
                    else:
                        emit('player_option', [dict_options['check'], emit_call_value, False, False], room=player_id)

                    decision = yield 'wait_for_player_decision'

                elif player.kind == 'bot':

                    n_fold = [gamer.live and gamer.alin for gamer in player_list].count(True)
                    n_player_in_round = number_player - n_fold

                    bot = AI(player.cards, dict_options, call_value, min_raise, max_raise, pot, n_player_in_round,
                             common_cards)
                    decision = bot.decision()

                elif player.kind == 'ai':
                    # DNN will make a decision based on: probability win, prob. tie, pot, stage of game
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

                    # observation = [probability win, p. tie, pot, preflop, flop, turn, river]

                    observation = [p_win, p_tie, pot/2000]
                    observation.extend(stage_round)

                    print('observation vector: ', observation)
                    model = load_model('models/model_20002epoch-1688915279.303047.h5')

                    # numpy
                    # best_action_index = np.argmax(model.predict(np.array(observation).reshape(1, 7)))

                    # without numpy
                    best_action_index = custom_argmax(model.predict([observation])[0])

                    # Needs best action from DNN approximate to best possible action in state

                    # There are 5 possible set of action
                    optimal_bet = best_action_index * 25
                    if optimal_bet > player.stack:
                        optimal_bet = player.stack

                    # 1 set
                    if dict_options['check'] and dict_options['raise']:
                        if optimal_bet < abs(optimal_bet - min_raise):
                            decision = ['check']
                        elif min_raise <= optimal_bet <= max_raise:
                            decision = ['raise', optimal_bet]
                        else:
                            decision = ['raise', min_raise]

                    # 2 set
                    elif dict_options['call'] and dict_options['raise']:
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
                        if optimal_bet < abs(call_value - optimal_bet):
                            decision = ['fold']
                        elif abs(optimal_bet - player.stack) < abs(optimal_bet - call_value):
                            decision = ['all-in']
                        else:
                            decision = ['call']

                    # 4 set
                    elif dict_options['check'] and not dict_options['raise']:
                        if optimal_bet < abs(optimal_bet - player.stack):
                            decision = ['check']
                        else:
                            decision = ['all-in']

                    # 5 set
                    elif not dict_options['call'] and not dict_options['check'] and not dict_options['raise']:
                        if optimal_bet < abs(optimal_bet - player.stack):
                            decision = ['fold']
                        else:
                            decision = ['all-in']

                elif player.kind == 'gpt':
                    # GPT will make decision based on information:
                    # stage round, own cards, common cards, pot, bet of opponent.
                    # First ask about decision: check, call, all-in, raise
                    # If he chooses raise then we ask how much raise
                    decision = None

                    # Create first stage prompt
                    if common_cards is None:
                        stage_round = 'Preflop'
                    elif len(common_cards) == 3:
                        stage_round = 'Flop'
                    elif len(common_cards) == 4:
                        stage_round = 'Turn'
                    else:
                        stage_round = 'River'

                    # ex. common_cards = ['AS', '2C', '5D']
                    if common_cards is None:
                        info_stage = 'Preflop. '
                    else:
                        name_cards = ', '.join(common_cards)
                        info_stage = stage_round + 'cards are ' + name_cards + '. '

                    name_player_cards = ', '.join(player.cards)
                    first_prompt = 'Heads-Up Texas Holdem. Blinds are ' + str(SB) + '/' + str(BB) + '. Pot is ' + \
                                   str(pot) + '. ' + info_stage + 'I have ' + name_player_cards + '. '

                    if dict_options['call']:
                        info_opponent_raise = 'Opponent raise ' + str(call_value) + '. '
                        first_prompt += info_opponent_raise

                    # prepare text available option
                    if dict_options['check']:
                        dict_options['fold'] = False
                    true_keys = [f"'{key}'" for key, value in dict_options.items() if value]
                    text_question = 'Answer with one word: ' + ', '.join(true_keys)

                    option_prompt = first_prompt + text_question

                    counter_try_option = 0
                    max_counter_try_option = 5
                    success_try_option = False

                    # Try to get correct response several times
                    while counter_try_option < max_counter_try_option and not success_try_option:

                        counter_try_option += 1

                        # CONNECT API GPT HERE response -> generate from option_prompt

                        response = get_content(option_prompt)
                        if show_game:
                            print('Response 1 from GPT:', response)
                        # process respond to decision
                        # text -> list of word
                        # check the words
                        respond_words = response.split()

                        # process first step

                        if 'check' in respond_words:
                            decision = ['check']
                            success_try_option = True
                        elif 'fold' in respond_words:
                            decision = ['fold']
                            success_try_option = True
                        elif 'call' in respond_words:
                            decision = ['call']
                            success_try_option = True
                        elif 'raise' in respond_words:
                            decision = ['raise', None]

                            success_try_option = True

                            counter_try_raise_val = 0
                            max_counter_try_raise_val = 5
                            success_try_val = False

                            # ask second question about how much raise
                            decision_prompt_how_raise = first_prompt + 'Try ' \
                                                                       'selecting a raise. Answer only with one number'

                            while counter_try_raise_val < max_counter_try_raise_val and not success_try_val:
                                counter_try_raise_val += 1

                                # print('prompt how mauch raise?: ', decision_prompt_how_raise)

                                # respond_how_much -> generate for decision_prompt_how_raise

                                respond_how_much = get_content(decision_prompt_how_raise)
                                if show_game:
                                    print('Response 2 from GPT:', respond_how_much)

                                # process respond
                                respond_words = respond_how_much.split()

                                int_elements = [element for element in respond_words if element.isdigit()]
                                raise_value = None

                                if int_elements:
                                    raise_value = int(int_elements[0])

                                if raise_value is not None:
                                    success_try_val = True
                                    # this is value which choose GPT
                                    # but now need to compare with available raise value

                                    if min_raise < raise_value < max_raise:
                                        available_raise_value = raise_value
                                    elif raise_value < min_raise:
                                        available_raise_value = min_raise
                                    elif raise_value > max_raise:
                                        available_raise_value = max_raise

                                    decision = ['raise', available_raise_value]

                    # Check if gpt returns correct answer, if not handle this

                    if decision is None:
                        if dict_options['check']:
                            decision = ['check']
                        elif dict_options['call']:
                            decision = [random.choice(['call', 'fold'])]
                        else:
                            decision = ['fold']

                    if decision[0] == 'raise':
                        if decision[1] is None:
                            decision[1] = min_raise

                    print('gpt decision', decision)

                # Now we have decision from one of player: human, bot, ai, gpt

                # Processing of player decision

                if decision[0] == 'raise':
                    chips = int(decision[1])
                decision = decision[0]

                if show_game:
                    if decision == 'raise':
                        print("{} stack: {} decision: {} {}".format(player.name, player.stack, decision, chips))
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
                        if gamer.live and gamer.decision:
                            gamer.decision = False
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()

                # Update info at the client

                emit('update_bet', [player.name, player.bet_auction], room=player_id)
                emit('update_stack', [player.name, player.stack], room=player_id)
                emit('update_pot', [sum([player.input_stack for player in player_list])], room=player_id)

                if decision == 'raise':
                    text_decision = 'raise ' + str(chips) + "$"
                elif decision == 'call':
                    text_decision = 'call ' + str(chips) + "$"
                elif decision == 'all-in':
                    text_decision = 'all-in for ' + str(player.input_stack) + "$"
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

