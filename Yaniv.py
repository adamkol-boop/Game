import random
import helper


class Yaniv:

    """
    THE CARDS:
        CLUBS:
            0 = Ace CLUBS
            1 = 2 CLUBS
            2 = 3 CLUBS
            3 = 4 CLUBS
            4 = 5 CLUBS
            5 = 6 CLUBS
            6 = 7 CLUBS
            7 = 8 CLUBS
            8  = 9 CLUBS
            9 = 10 CLUBS
            10 = jack (J) CLUBS
            11 = queen (Q) CLUBS
            12 = king (K) CLUBS

        DIAMONDS:
            13 = Ace DIAMONDS
            14 = 2 DIAMONDS
            15 = 3 DIAMONDS
            16 = 4 DIAMONDS
            17 = 5 DIAMONDS
            18 = 6 DIAMONDS
            19 = 7 DIAMONDS
            20 = 8 DIAMONDS
            21  = 9 DIAMONDS
            22 = 10 DIAMONDS
            23 = jack (J) DIAMONDS
            24 = queen (Q) DIAMONDS
            25 = king (K) DIAMONDS

        HEARTS:
            26 = Ace HEARTS
            27 = 2 HEARTS
            28 = 3 HEARTS
            29 = 4 HEARTS
            30 = 5 HEARTS
            31 = 6 HEARTS
            32 = 7 HEARTS
            33 = 8 HEARTS
            34  = 9 HEARTS
            35 = 10 HEARTS
            36 = jack (J) HEARTS
            37 = queen (Q) HEARTS
            38 = king (K) HEARTS

        SPADES:
            39 = Ace SPADES
            40 = 2 SPADES
            41 = 3 SPADES
            42 = 4 SPADES
            43 = 5 SPADES
            44 = 6 SPADES
            45 = 7 SPADES
            46 = 8 SPADES
            47  = 9 SPADES
            48 = 10 SPADES
            49 = jack (J) SPADES
            50 = queen (Q) SPADES
            51 = king (K) SPADES

        52 = JOKER
        53 = JOKER
    """

    def help(self):
        """returns all the functions available"""
        res = ""

    def __init__(self):
        ''' the cards that are in use
        represented by 1, and the rest
        of them are defaultly by 0 '''
        self.in_use = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0]
        self.out_of_use = []
        self.winner = None

    def deal(self, cards_num):
        """the function gets the number
        of the cards that the player needs,
        and returns a list of the given cards"""

        cards = []
        while cards_num > 0:

            x = random.randint(0, 53)
            if self.in_use[x] == 0:
                self.in_use[x] += 1
                cards.append(x)
                cards_num -= 1

        return cards

    def who_starts(self, players_num):
        # returns a number: who starts
        return random.randint(0, players_num)

    @staticmethod
    def num_to_card(card_num):
        """the function gets the card number
            from 1 to 53 and returns the actual
            card value --> 43 its 5"""
        card_num = int(card_num)
        if card_num <= 51:
            return (card_num % 13) + 1
        return 0

    def sum_cards(self, cards_list):
        """The function gets a list of cards
            and returns the sum of the card values"""
        sum = 0
        for num in cards_list:
            if num > 51:  # means it's Joker
                sum += 0
            else:
                sum += self.num_to_card(num)

        return sum

    def going_out(self, cards):
        """the func gets an array of cards
            that a player just used, and adds
            them to the out of use array"""
        for card in cards:
            self.out_of_use.append(int(card))
        # print(self.out_of_use)

    def is_same_sign(self, cards):
        """the function gets a list of cards
            and checks if they are with the same
            sign, returns True or False"""

        jokers = 0
        w_o_jokers = []
        for card in cards:
            if self.num_to_card(int(card)) == 0:
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

    def ascend(self, cards, jokers):
        """the recursion function gets an array of cards,
            and the number of the jokers, returns true if the
             combination is valid, and false if not"""

        #print("sortn' in ascend", jokers)
        sort = sorted(cards)  # sorting by ascend order
        #print(sort)
        for i in range(0, len(sort)):
            sort[i] = int(sort[i])

        if jokers == 2:
            sort[-1] = 60
            sort[-2] = 61
        if jokers == 1:
            sort[-1] = 60
        if len(sort) == 1 and not (jokers < 0):
            return True
        if sort[0] == sort[1] - 1:
            return self.ascend(sort[1:], jokers)
        if sort[0] == sort[1] - 2:
            return self.ascend(sort[1:], jokers - 1)
        if sort[0] == sort[1] - 3:
            return self.ascend(sort[1:], jokers - 2)
        if sort[1] > 51 and not (jokers < 0):
            return True
        return False

    def check_valid(self, cards):
        """The func gets an array of cards
            and checks if the combination is
            valid, returns True or False"""

        if len(cards) == 1:  # one card
            return True
        if len(cards) == 2:  # two cards
            if ((self.num_to_card(int(cards[0])) == self.num_to_card(int(cards[1]))) or  # two same cards
                    (int(cards[0]) > 51) or  # any card and a joker
                    (int(cards[1])) > 51):  # any card and a joker
                return True
            return False

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
            if self.num_to_card(int(card)) == self.num_to_card(int(sort[0])) or int(card) > 51:
                index += 1
        if index == len(cards):
            return True

        #  check ascend order
        if not self.is_same_sign(cards):
            print('Here')
            return False

        #print("accend left")
        return self.ascend(cards, jokers)

    def turn(self, card_nums):
        pass

# def main():
#     game = Yaniv()
#     p1 = game.deal(5)
#     p2 = game.deal(5)
#
#     print('Player 1: ' + str(p1) + "\nPlayer 2: " + str(p2))
#
#     while game.winner is None:
#         p1_turn = input("P1 choose card\s: ")
#         chosen_indexes = p1_turn.split(", ")
#         chosen = []
#         for num in chosen_indexes:
#            chosen.append()
#         print(chosen)
#         if not game.check_valid(chosen):
#            print('not a good pick')


    # cards = game.deal(5)
    # print(cards)
    # print(game.in_use)
    # print(game.sum_cards(cards))

    #helper.print_funcs()

#if __name__ == '__main__':
    #main()

#game = Yaniv()
#print(Yaniv.check_valid(game, [22,23,24,25, 53]))
