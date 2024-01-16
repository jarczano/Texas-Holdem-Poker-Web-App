# Instead calculate each time probability of win and tie for preflop, read value from database

def probability_array(suited):

    if suited:
        name = 'models/probability_suited.txt'
    else:
        name = 'models/probability_unsuited.txt'
    with open(name, 'r') as file:
        lines = file.readlines()

    return [[float(item) for item in line.strip().split(', ')] for line in lines]


def probability(cards):
    suited = False
    if cards[0][1] == cards[1][1]:
        suited = True

    dict_figure = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    handfigure = [card[0] for card in cards]

    handfigure = [dict_figure.get(handfigure[i], handfigure[i]) for i in range(2)]
    handfigure = sorted([int(handfigure[i]) for i in range(2)])
    x,y = handfigure[0], handfigure[1]

    if suited:
        index = 0.5 * (27 * x - 54 - x ** 2) + y -1
        list_probability = probability_array(suited=True)
    else:
        index = 0.5 * (29 * x - 56 - x ** 2) + y - 1

        list_probability = probability_array(suited=False)

    p_win, p_tie = list_probability[int(index)]
    return p_win, p_tie