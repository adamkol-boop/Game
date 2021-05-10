from tabulate import tabulate


def print_funcs():
    print(tabulate([['deal(cards_num)', 'Number of cards', 'Array of the random cards',
                     'x = deal(4)\nx = [13, 42, 6,23]'],

                    ['who_starts(players_num)', 'Number of players', 'A random number which represents who starts',
                     'x = who_starts(3)\nx = 1'],

                    ['num_to_card(card_num)', 'Card number from 0 to 53', 'The actual card value. For example',
                     'x = num_to_card(34)\nx = 9'],

                    ['sum_cards(cards_list)', 'Array of card numbers', 'The sum of the card values',
                     'x = sum_cards([3, 46, 31, 53, 12])\nx = 31'],

                    ['going_out(cards)', 'Array of card numbers', '-',
                     'going_out([3, 16])\nself.out_of_use = [3, 16]\n'],

                    ['check_valid(cards)', 'Array of card numbers', 'True, if the combination of the cards\n'
                                                                    'and False if its invalid',
                     'x = check_valid([1, 11, 12])\nx = False\n\ny = check_valid([26, 40, 41, 16])\ny = True']],

                    ["func()", "gets", "returns", "example"], "fancy_grid"))
