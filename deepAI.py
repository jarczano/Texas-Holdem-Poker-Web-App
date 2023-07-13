class Bot:
    def __init__(self):
        self.cards = ''
        self.score = 0
        self.hand = ''


def probability_win(own_cards, n_players, common_cards=None):
    # Bot calculates the probability of winning simulating 5,000 games with such cards
    import random
    from poker_score import players_score

    number_games = 1000
    n_win = 0
    n_tie = 0
    ai = Bot()
    ai.cards = own_cards

    deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S',
            '5S',
            '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H',
            '9H',
            'TH', 'JH', 'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD',
            'KD', 'AD']

    [deck.remove(card) for card in ai.cards]

    if common_cards is not None:
        [deck.remove(card) for card in common_cards]

    # create artificial bots as many as there are opponents
    list_bots = []  # czy tego sie nie dało jakos ladnioe zapisywac
    for nbot in range(n_players - 1):
        list_bots.append(Bot())

    # simulating game
    for i in range(number_games):
        bot_deck = deck.copy()
        for bot in list_bots:
            bot.cards = random.sample(bot_deck, 2)
            [bot_deck.remove(bot.cards[i]) for i in range(2)]

        if common_cards is None:
            table = random.sample(bot_deck, 5)
        else:
            table = common_cards + random.sample(bot_deck, 5 - len(common_cards))

        players_score(list_bots, table)
        players_score([ai], table)

        list_score = []
        for bot in list_bots:
            list_score.append(bot.score)

        if ai.score > max(list_score):
            n_win += 1
        elif ai.score == max(list_score):
            n_tie += 1

    return n_win / number_games, n_tie / number_games

#own_cards = ['AS', 'KD']
#common_cards = ['QS', 'KH', 'AC']
#n_players = 2
#p_win, p_tie = probability_win(own_cards, n_players, common_cards)
#print(p_win, p_tie)
