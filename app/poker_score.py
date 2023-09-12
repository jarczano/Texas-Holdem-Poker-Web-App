import itertools


def hand(composition):
    """
    Function calculate the score of hand composition.
    Method of calculating score is relative, just better composition gets higher score.
    :param composition: list of five cards. ex. ['2D', '3C', 'AH' , 'AC', '7D']
    :return: score of composition and name of hand ranking
    """
    # Split colors and figures cards
    handfigure = [card[0] for card in composition]
    handcolor = [card[1] for card in composition]

    # Change card figures to a numbers
    dict_figure = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    handfigure = [dict_figure.get(handfigure[i], handfigure[i]) for i in range(5)]

    # Sort the cards
    handfigure = sorted([int(handfigure[i]) for i in range(5)])

    # Check straight
    if [handfigure[i] - handfigure[0] for i in range(5)] == [0, 1, 2, 3, 4] or handfigure == [2, 3, 4, 5, 14]:
        straight = True
    else:
        straight = False

    # Condition for Royal Flush
    if handfigure == [10, 11, 12, 13, 14] and len(set(handcolor)) == 1:
        score = 180
        name_poker_hand = 'Royal flush'

    # Condition Straight Flush
    # score from 166 to 173
    elif straight is True and len(set(handcolor)) == 1:
        score = 160 + handfigure[4]
        name_poker_hand = "Straight Flush"

    # Condition four of kind
    # score from 142.03 to 154.13
    elif handfigure.count(handfigure[2]) == 4:
        if handfigure.count(handfigure[0]) == 1:
            score = 140 + handfigure[1] + handfigure[0] / 100
        else:
            score = 140 + handfigure[0] + handfigure[4] / 100
        name_poker_hand = 'Four of kind'

    # Condition full house
    # score from 122.02 to 134.13
    elif len(set(handfigure)) == 2 and handfigure.count(handfigure[2]) != 4:
        if handfigure.count(handfigure[0]) == 2:
            score = 120 + handfigure[2] + handfigure[0] / 100
        else:
            score = 120 + handfigure[0] + handfigure[3] / 100
        name_poker_hand = "Full house"

    # Condition for Flush
    # score from 100.75432 to 101.54319
    elif len(set(handcolor)) == 1:
        score = 100 + handfigure[4] / 10 + handfigure[3] / 100 + handfigure[2] / 1000 + handfigure[1] / 10000 + handfigure[0] / 100000
        name_poker_hand = "Flush"

    # Condition for Straight
    # score from 80 to 94
    elif straight is True:
        if handfigure == [2, 3, 4, 5, 14]:
            score = 80
        else:
            score = 80 + handfigure[4]
        name_poker_hand = "Straight"

    # Condition for three of kind
    # score from 62.043 to 74.142
    elif handfigure.count(handfigure[2]) == 3 and len(set(handfigure)) == 3:
        handfigure_set = list(set(handfigure))
        handfigure_set.remove(handfigure[2])
        score = 60 + handfigure[2] + handfigure_set[1] / 100 + handfigure_set[0] / 1000
        name_poker_hand = 'Three of kind'

    # Condition for two pair
    # score from 43.24 to 55.419999999999995
    elif handfigure.count(handfigure[1]) == 2 and handfigure.count(handfigure[3]) == 2:
        handfigure_set = list(set(handfigure))
        handfigure_set.remove(handfigure[1])
        handfigure_set.remove(handfigure[3])
        score = 40 + handfigure[3] + handfigure[1] / 10 + handfigure_set[0] / 100
        name_poker_hand = "Two pair"

    # Condition for pair
    # score from 22.05043 to 34.13131
    elif len(set(handfigure)) == 4:
        if handfigure.count(handfigure[1]) == 2:
            handfigure_set = list(set(handfigure))
            handfigure_set.remove(handfigure[1])
            score = 20 + handfigure[1] + handfigure_set[2] / 100 + handfigure_set[1] / 10000 + handfigure_set[0] / 100000
        elif handfigure.count(handfigure[3]) == 2:
            handfigure_set = list(set(handfigure))
            handfigure_set.remove(handfigure[3])
            score = 20 + handfigure[3] + handfigure_set[2] / 100 + handfigure_set[1] / 10000 + handfigure_set[0] / 100000
        name_poker_hand = "Pair"

    # Condition for high card
    # score from 7.543200000000001 to 15.431899999999999
    elif len(set(handfigure)) == 5:
        score = handfigure[4] + handfigure[3] / 10 + handfigure[2] / 100 + handfigure[1] / 1000 + handfigure[0] / 10000
        name_poker_hand = "High card"

    return score, name_poker_hand


def players_score(player_list, common_cards):
    """
    Function calculates and assigns each player a score of his cards and name of hand ranking
    :param player_list: list of players for whom score are to be calculated
    :param common_cards:
    :return: nothing, function assigns a score to player object
    """

    for player in player_list:
        best_score, best_hand = 0, ''
        cards_combinations = list(itertools.combinations(common_cards + player.cards, 5))
        for combination in cards_combinations:
            combination_score, combination_name = hand(combination)
            if combination_score > best_score:
                best_score = combination_score
                player.score, player.hand = best_score, combination_name
