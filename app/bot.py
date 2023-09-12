import random


class Bot:
    def __init__(self):
        self.cards = ''
        self.score = 0
        self.hand = ''


class AI:
    """
    Class for math bot
    """
    def __init__(self, own_cards, dict_options, call_value, min_raise, max_raise, pot, n_players, common_cards=None):
        self.own_cards = own_cards  # ex. ['AS', '4C']
        self.common_cards = common_cards
        self.dict_options = dict_options
        self.call_value = call_value
        self.min_raise = min_raise
        self.max_raise = max_raise
        self.pot = pot
        self.n_players = n_players

    def probability_win(self):
        """
        Calculates the probability of winning simulating n games with such own cards
        :return: probability of win, probability of tie
        """

        import random
        from app.poker_score import players_score

        number_games = 500
        n_win = 0
        n_tie = 0
        ai = Bot()
        ai.cards = self.own_cards

        deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S',
                '5S',
                '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H',
                '9H',
                'TH', 'JH', 'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD',
                'KD', 'AD']

        [deck.remove(card) for card in ai.cards]

        if self.common_cards is not None:
            [deck.remove(card) for card in self.common_cards]

        # create artificial bots as many as there are opponents
        list_bots = []
        for nbot in range(self.n_players - 1):
            list_bots.append(Bot())

        # simulating games
        for i in range(number_games):
            bot_deck = deck.copy()
            for bot in list_bots:
                bot.cards = random.sample(bot_deck, 2)
                [bot_deck.remove(bot.cards[i]) for i in range(2)]

            if self.common_cards is None:
                table = random.sample(bot_deck, 5)
            else:
                table = self.common_cards + random.sample(bot_deck, 5 - len(self.common_cards))

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

    def decision(self):
        """
        Function make decision based on probability win, p. tie, pot.
        Function sometimes makes a random decision so as not to be a predictable.
        :return: bot decision how to play
        """

        from setting import BB
        p_win, p_tie = self.probability_win()
        rais = 0

        if p_win > 0.5:
            if self.dict_options['raise']:
                factor = int(max(BB, self.pot / 8))
                if p_win < 0.75:
                    rais = int((12 * p_win - 5) * factor)
                else:
                    rais = int((-12 * p_win + 13) * factor)

                if rais < self.min_raise:
                    rais = self.min_raise
                    decision = 'raise'
                elif rais > self.max_raise:
                    rais = self.max_raise
                    decision = 'all-in'
                else:
                    decision = 'raise'
                    rais = int(rais)
            else:
                decision = 'all-in'
                rais = self.max_raise
        else:
            max_call = int(p_win * self.pot + p_tie * self.pot / self.n_players)
            if self.dict_options['check']:
                # sometimes 2 of 10 case instead of check make raise
                random_raise = random.randint(1, 10)
                if random_raise > 8:
                    if self.min_raise < max_call: # jeszcze warunker ze raise < self.max_raise
                        rais = min(max_call, self.max_raise)
                        decision = 'raise'
                    else:
                        decision = 'check'
                else:
                    decision = 'check'
            else:
                if max_call < self.call_value:
                    decision = 'fold'
                else:
                    # sometimes 2 of 10 case instead of call make raise
                    random_raise = random.randint(1, 10)
                    if random_raise > 8:
                        if self.min_raise < max_call:
                            rais = min(max_call, self.max_raise)
                            decision = 'raise'
                        else:
                            if self.call_value < self.max_raise:
                                decision = 'call'
                            else:
                                decision = 'all-in'
                    else:
                        if self.call_value < self.max_raise:
                            decision = 'call'
                        else:
                            decision = 'all-in'

        if decision == 'raise':
            rais = AI._round_to_multiple(rais, 25)

        return [decision, rais]

    @staticmethod
    def _round_to_multiple(number, multiple):
        """
        the function approximates a number to a given multiple
        ex: (69, 25) = 75
        ex: (59, 25) = 50
        :param number:
        :param multiple:
        :return:approximate number
        """
        total = number // multiple
        if (number - total * multiple) / multiple > 0.5:
            total += 1
        return total * multiple
