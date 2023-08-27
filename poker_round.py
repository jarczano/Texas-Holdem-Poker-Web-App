import random
import time

from auction import auction
from poker_score import players_score
from split_pot import one_player_win, change_players_positions, split_pot
from player_class import Player
from setting import BB, SB, show_game, time_pause_round_end
from flask_socketio import emit


def poker_round(player_id):

    player_list_chair = Player.player_list_chair
    player_list = Player.player_list

    emit('message_decision', 'New round', room=player_id)

    # Take blinds from players
    if player_list[-1].stack > BB:
        player_list[-1].blind(BB)

        emit('message_decision', player_list[-1].name + ' big blind ' + str(BB) + "$", room=player_id)
    else:
        player_list[-1].blind(player_list[-1].stack)
        player_list[-1].allin()

        emit('message_decision', player_list[-1].name + ' big blind ' + player_list[-1].input_stack + "$", room=player_id)
        emit('message_decision', player_list[-1].name + ' short stack all-in ' + player_list[-1].input_stack, room=player_id)

    if player_list[-2].stack > SB:
        player_list[-2].blind(SB)

        emit('message_decision', player_list[-2].name + ' small blind ' + str(SB) + "$", room=player_id)
    else:
        player_list[-2].blind(player_list[-2].stack)
        player_list[-2].allin()

        emit('message_decision', player_list[-2].name + ' small blind ' + player_list[-2].input_stack + "$", room=player_id)
        emit('message_decision', player_list[-2].name + ' short stack all-in ' + player_list[-2].input_stack, room=player_id)


    #join_room(player_id)
    # send info about blind to the client
    for player in player_list_chair:

        #socketio.emit('update_bet', [player.name, player.input_stack])

        emit('update_bet', [player.name, player.input_stack], room=player_id)
        emit('update_stack', [player.name, player.stack], room=player_id)

    # send info about pot
    pot = sum([player.input_stack for player in player_list])
    emit('update_pot', [pot], room=player_id)

    if show_game:
        print(player_list[-1].name, 'BB')
        print(player_list[-2].name, 'SB')

    # Create a deck of cards
    deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S', '5S', '6S',
            '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH',
            'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

    # Deal the cards to the player
    for player in player_list_chair:
        player.cards = random.sample(deck, 2)
        [deck.remove(player.cards[i]) for i in range(2)]
        # send player card to the client
        if player.kind == 'human':
            emit('deal_player_cards', player.cards, room=player_id)
        else:
            emit('deal_opponent_cards', room=player_id)

    if show_game:
        for player in player_list:
            print(player.name, player.cards)

    # Check how many players are in the game and all-in
    number_live_players = sum([player.live for player in player_list])  # 1
    number_allin_players = sum([player.alin for player in player_list]) # 0

    if number_live_players > 1:
        # First auction

        if show_game:
            print("Preflop")

        yield from auction(player_id)

        # reset bet auction
        for player in player_list:
            emit('update_bet', [player.name, 0], room=player_id)


        #for player in player_list:
        #    player.reward = 0
    # Check how many players are in the game and all-in
    number_live_players = sum([player.live for player in player_list])  # 1
    number_allin_players = sum([player.alin for player in player_list]) # 0

    #for player in player_list:
   #     player.reward = 0

    # change order decision player
    if len(player_list_chair) == 2:
        shift_decision = -1
    else:
        shift_decision = -2

    # If there is only one player left in the game, he wins
    if number_live_players + number_allin_players == 1:

        one_player_win(player_id)
        # end of round
        time.sleep(time_pause_round_end)
        # hide opponent decision
        emit('hide_opponent_decision', room=player_id)
    else:
        # Flop
        emit('hide_opponent_decision', room=player_id)
        flop = random.sample(deck, 3)
        [deck.remove(flop[i]) for i in range(3)]
        common_cards = flop

        # send flop cards to client
        emit('deal_flop_cards', common_cards, room=player_id)

        if show_game:
            print("Flop cards: {}".format(flop))

        # Change order decision players
        change_players_positions(shift_decision)

        if number_live_players > 1:

            # Second auction
            yield from auction(player_id, common_cards)

            # reset auction bet
            for player in player_list:
                emit('update_bet', [player.name, 0], room=player_id)


        # Check how many players are in the game and all-in
        number_live_players = sum([player.live for player in player_list])
        number_allin_players = sum([player.alin for player in player_list])

        # If there is only one player left in the game, he wins
        if number_live_players + number_allin_players == 1:

            one_player_win(player_id)

            # end of round
            time.sleep(time_pause_round_end)
            # hide opponent decision
            emit('hide_opponent_decision', room=player_id)
            # Return to the original position
            change_players_positions(shift_decision)
        else:

            emit('hide_opponent_decision', room=player_id)
            # Deal the cards to the turn
            turn = random.sample(deck, 1)
            deck.remove(turn[0])
            common_cards = flop + turn

            # send turn card to client
            emit('deal_turn_card', turn, room=player_id)

            if show_game:
                print("Turn cards: {}".format(common_cards))
            #print('Turn: ', common_cards)

            if number_live_players > 1:
                # Third auction
                yield from auction(player_id, common_cards)

                # reset auction bet
                for player in player_list:
                    emit('update_bet', [player.name, 0], room=player_id)



            # Check how many players are in the game and all-in
            number_live_players = sum([player.live for player in player_list])
            number_allin_players = sum([player.alin for player in player_list])

            # If there is only one player left in the game, he wins
            if number_live_players + number_allin_players == 1:
                one_player_win(player_id)
                
                # end of round
                time.sleep(time_pause_round_end)
                # hide opponent decision
                emit('hide_opponent_decision', room=player_id)
                change_players_positions(shift_decision)
            else:
                emit('hide_opponent_decision', room=player_id)
                # Deal the cards to the river
                river = random.sample(deck, 1)
                deck.remove(river[0])
                common_cards += river

                # send river card to client
                emit('deal_river_card', river, room=player_id)

                if show_game:
                    print("River cards: {}".format(common_cards))

                if number_live_players > 1:
                    # Last auction
                    yield from auction(player_id, common_cards)

                        # reset auction bet
                    for player in player_list:
                        emit('update_bet', [player.name, 0], room=player_id)


                # Check how many players are in the game and all-in
                number_live_players = sum([player.live for player in player_list])
                number_allin_players = sum([player.alin for player in player_list])

                # If there is only one player left in the game, he wins
                if number_live_players + number_allin_players == 1:

                    # Return to the original position
                    one_player_win(player_id)

                    # end of round
                    time.sleep(time_pause_round_end)
                     # hide opponent decision
                    emit('hide_opponent_decision', room=player_id)
                    change_players_positions(shift_decision)
                else:

                    # Send message to show down client
                    for player in player_list:
                        if player.kind != 'human':
                            emit('show_down', player.cards, room=player_id)

                    # Calculate score players
                    players_score(player_list_chair, common_cards)

                    # Split pot
                    split_pot(player_id)

                    # end of round
                    time.sleep(time_pause_round_end)

                    # Return players to the original position
                    change_players_positions(shift_decision)


