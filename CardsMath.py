'''The class collects all the functions from Yaniv
that can be static and there no need for them to be
in this class'''

def num_to_card(card_num):
        """the function gets the card number
            from 1 to 53 and returns the actual
            card value --> 43 its 5"""
        card_num = int(card_num)
        if card_num <= 51:
            return (card_num % 13) + 1
        return 0

def sum_cards(cards_list):
        """The function gets a list of cards
            and returns the sum of the card values"""
        sum = 0
        for num in cards_list:
            if int(num) > 51:  # means it's Joker
                sum += 0
            else:
                sum += num_to_card(int(num))
        return sum

def is_same_sign(cards):
    """the function gets a list of cards
        and checks if they are with the same
        sign, returns True or False"""

    jokers = 0
    w_o_jokers = []
    for card in cards:
        if num_to_card(int(card)) == 0:
            jokers += 1
        else:
            w_o_jokers.append(int(card))

    w_o_jokers = sorted(w_o_jokers)
    print("whitout jokers: ", w_o_jokers)
    if w_o_jokers[0] <= 12:  # if the cards are CLUBS
        if w_o_jokers[-1] > 12:
            return False
    if w_o_jokers[0] <= 25:  # if the cards are DIAMONDS
        if w_o_jokers[-1] > 25:
            return False
    if w_o_jokers[0] <= 38:  # HEARTS
        if w_o_jokers[-1] > 38:
            return False
    if w_o_jokers[0] <= 51:
        if w_o_jokers[-1] > 51:
            return False
    return True

def ascend(cards, jokers, order, times_repeated):
    """the recursion function gets an array of cards,
        and the number of the jokers, returns true if the
         combination is valid, and false if not"""

    #print("sortn' in ascend", jokers)
    sort = sorted(cards)  # sorting by ascend order
    #print(sort)
    for i in range(0, len(sort)):
        sort[i] = int(sort[i])

    if jokers == 2 and times_repeated == 0:
        sort[-1] = sort[-1] + 10
        sort[-2] = sort[-2] + 10
    if jokers == 1 and times_repeated == 0:
        sort[-1] = sort[-1] + 10
    if jokers < 0:
        return False, cards
    if len(sort) == 1:
        if sort[0] >= 62:
            order.append(sort[0] - 10)
        else:
            order.append(sort[0])
        return True, order
    if sort[0] == sort[1] - 1:  # real valid accend
        order.append(sort[0])
        return ascend(sort[1:], jokers, order, times_repeated + 1)
    if sort[0] == sort[1] - 2:  # joker between them
        order.append(sort[0])
        if (sort[-1]) >= 62:
            order.append(sort[-1] - 10)
        return ascend(sort[1:], jokers - 1, order, times_repeated + 1)
    if sort[0] == sort[1] - 3:
        order.append(sort[0])
        if (sort[-1]) >= 62 and sort[-2] >= 62:
            order.append(sort[-1] - 10)
            order.append(sort[-2] - 10)
        return ascend(sort[1:], jokers - 2, order, times_repeated + 1)
    if sort[1] > 51 and not (jokers < 0):
        order.append(sort[0])
        print("final order:", order, "sort left is:", sort)
        if len(sort) == 2:
            if (sort[1] - 10) not in order:
                order.append(sort[1] - 10)
        else:
            if (sort[1] - 10) not in order:
                order.append(sort[1] - 10)
            if (sort[2] - 10) not in order:
                order.append(sort[2] - 10)
        return True, order
    return False, order

def check_valid(cards):
        """The func gets an array of cards
            and checks if the combination is
            valid, returns True or False for validation, and the cards"""

        if len(cards) == 1:  # one card
            return True, cards
        if len(cards) == 2:  # two cards
            if ((num_to_card(int(cards[0])) == num_to_card(int(cards[1]))) or  # two same cards
                    (int(cards[0]) > 51) or  # any card and a joker
                    (int(cards[1])) > 51):  # any card and a joker
                return True, cards
            return False, cards

        #  3 or more: all same number/ascending order
        # check how many jokers
        jokers = 0
        for card in cards:
            #print(int(card))
            #print(self.num_to_card(card))
            if int(card) > 51:
                jokers += 1
                #print("YESSSSSSSSSSIR")
        #print(f'[THERE ARE {jokers} JOKERS]')

        #  check if all same number
        sort = sorted(cards)
        #print(f'[THE SORTED CARDS: {sort}]')
        index = 0
        for card in sort:
            if num_to_card(int(card)) == num_to_card(int(sort[0])) or int(card) > 51:
                index += 1
        if index == len(cards):
            return True, cards

        #  check ascend order
        if not is_same_sign(cards):
            #print('Here')
            return False, cards

        #print("accend left")
        return ascend(cards, jokers, [], 0)
