import socket
import threading
import Yaniv
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
YANIV_MESSAGE = 'yaniv'
ASAF_MESSAGE = 'asaf'
NOT_YOU_YANIV_MESSAGE = 'NYYANIV'


queue = []
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"THREAD [NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        data = conn.recv(1024).decode(FORMAT)
        if data == DISCONNECT_MESSAGE:
            connected = False
        queue.append(data)
        print("[THE QUEUE IS NOW: ", queue)
        print(f"[{addr}] {data}")
        #conn.send("[DATA RECEIVED]".encode(FORMAT))


    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}\n")
    count = 0
    while count < 10:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        count += 1
    print(f"[FINISHED {count} CONNECTIONS]\n")

def wait_for_msg():
    while len(queue) == 0:
        pass
    return queue[0]

def all_cards_used(game):
    '''the function gets a game type Yaniv
    and returns false if there are still cards in stack
    otherwise, returns true and clears the used cards into a new stack'''
    for card in game.in_use:
        if card == 0:
            return False
    # if not returned yet, means the stack is empty
    for card_num in game.out_of_use:
        game.in_use[card_num] = 0
    return True

def broadcast(clients, message):
    for client in clients:
        client.send(f'BROADCAST&{message}'.encode(FORMAT))

def turn(player, p_cards, game, last_turn_cards):
    '''the function  handles a turn. it ends only when
    the player has made a valid turn'''
    chosen_cards = []
    time.sleep(1)
    turn_msg = "It's your turn!"

    player.send(f'LC&{last_turn_cards}'.encode(FORMAT))
    print(f"[LAST TURN CARD SENT:] {last_turn_cards}")

    time.sleep(1)

    end_turn = False
    while not end_turn:


        player.send(f'TM&{turn_msg}'.encode(FORMAT))

        #time.sleep(1)

        # player.send(f'The last turn cards are: {last_turn_cards}'.encode(FORMAT))
        # print(f"[LAST TURN CARD SENT:] {last_turn_cards}")

        res = wait_for_msg()
        queue.clear()
        if res == YANIV_MESSAGE:
            print("[PLAYER CALLED YANIV]")
            sum = game.sum_cards(p_cards)
            if sum <= 7:
                player.send('TM&VALID YANIV'.encode(FORMAT))
                print("[YANIV VERIFIED]")
                return YANIV_MESSAGE
            print("[INVALID]")
            turn_msg = "INVALID"
        else:
            chosen_cards = res.split(' ')
            print(f'Clients chosen cards: {chosen_cards}')

            valid_cards = game.check_valid(chosen_cards)
            if valid_cards:
                print('[VALID]')
                game.going_out(chosen_cards)
                for i in range(0, len(chosen_cards)):
                    p_cards.remove(int(chosen_cards[i]))
                print(f"[UPDATED CARDS] {p_cards}")

                turn_msg = 'VALID'
                player.send(f'TM&{turn_msg}'.encode(FORMAT))
                print("[TURN MES SENT]")

                #time.sleep(1)

                # current_players[who_starts].send(f'The last turn cards are: {last_turn_cards}'.encode(FORMAT))
                # print(f"[LAST TURN CARD SENT:] {last_turn_cards}")

                deck_or_last = wait_for_msg()
                queue.clear()

                if deck_or_last == 'DECK':
                    new_card = game.deal(1)
                    p_cards.append(new_card[0])
                    player.send(f"NC&You new cards: {p_cards}".encode(FORMAT))

                elif deck_or_last == 'LAST':
                    #current_players[who_starts].send(f'The last turn cards are: {last_turn_cards}'.encode(FORMAT))
                    res = wait_for_msg()
                    queue.clear()

                    #print(game.out_of_use)
                    game.out_of_use.remove(int(res))

                    p_cards.append(int(res))
                    player.send(f"NC&You new cards: {p_cards}".encode(FORMAT))

                #turn_msg = f"VALID Your updated cards: {all_cards[who_starts]}"



                end_turn = True

            if not valid_cards:
                print('[INVALID]')
                turn_msg = "INVALID"
    return chosen_cards


def list_to_string(card_list):
    p_cards_str = ''
    for card in card_list:
        p_cards_str += str(card) + ' '
    return p_cards_str

def game(clients):

    current_players = clients
    all_cards = []

    game = Yaniv.Yaniv()# New game created

    players = 0
    for player in clients:
        p_cards = game.deal(5)  # dealing cards in lists
        all_cards.append(p_cards)  # adding to all cards

        cards_str = list_to_string(p_cards)
        print(f"[P{players + 1}]'S CARDS] {cards_str}")

        player.send(f'SGC&{cards_str}'.encode(FORMAT))
        players += 1

    # changing the cards' format to string with spaces
    # p1_cards_str = ''
    # for card in p1_cards:
    #     p1_cards_str += str(card) + ' '
    #
    #
    # p2_cards_str = ''
    # for card in p2_cards:
    #     p2_cards_str += str(card) + ' '
    #
    # print('the cards of the first player are: ' + p1_cards_str)
    # print('the cards of the second player are: ' + p2_cards_str)
    #
    # # sending the players the cards
    # conn1.send(bytes(p1_cards_str, encoding='utf8'))
    # conn2.send(bytes(p2_cards_str, encoding='utf8'))

    who_starts = game.who_starts(len(clients) - 1)

    last_cards = game.deal(1)
    game.going_out(last_cards)

    match = True
    while match:
        last_cards = turn(clients[who_starts], all_cards[who_starts], game, last_cards)
        who_starts += 1

        if last_cards == YANIV_MESSAGE:
            who_starts -= 1
            match = False

        if who_starts == (len(clients)):
            who_starts = 0

        is_empty_stack = all_cards_used(game)
        if is_empty_stack:
            broadcast(clients, '\n[[[ReNeWiNg StAcK]]]\n')
            last_cards = game.deal(1)
            game.going_out(last_cards)

    # now sending for all

    winner = [game.sum_cards(all_cards[who_starts]), who_starts]
    for i in range(0, len(clients)):
        if i != who_starts:
            clients[i].send(NOT_YOU_YANIV_MESSAGE.encode(FORMAT))
            if game.sum_cards(all_cards[i]) <= winner[0]:
                winner = [game.sum_cards(all_cards[i]), i]

    if winner[1] == who_starts:
        for i in range(0, len(clients)):
            if i != who_starts:
                clients[i].send("LC&EML".encode(FORMAT))
            elif i == who_starts:
                clients[i].send("EM&CONGRATULATIONS Your YANIV approved!".encode(FORMAT))
    else:
        for i in range(0, len(clients)):
            if i == winner[1]:
                clients[i].send("LC&EMA".encode(FORMAT))
            elif i == who_starts:
                clients[i].send("EM&Oops, seems like you got ASAFed...".encode(FORMAT))
            else:
                clients[i].send("LC&EML".encode(FORMAT))

    # next_p = 0
    # if who_starts == 0:
    #     next_p = 1
    #
    # last_cards_2 = game.deal(1)
    # game.going_out(last_cards_2)
    # while True:
    #     last_cards_1 = turn(current_players, all_cards, who_starts, game, last_cards_2)
    #     if last_cards_1 == YANIV_MESSAGE:
    #         return
    #     last_cards_2 = turn(current_players, all_cards, next_p, game, last_cards_1)
    #     if last_cards_2 == YANIV_MESSAGE:
    #         return


    # turn = True
    # turn_msg = 'Its your turn!'
    #
    # match_is_on = True
    # while match_is_on:
    #     while turn:
    #         while len(queue) == 0:
    #             current_players[who_starts].send(turn_msg.encode(FORMAT))
    #             while True:
    #                 try:
    #                     chosen_cards = queue[0].split(' ')
    #                     time.sleep(1)
    #                     print("\nThe chosen cards: ", chosen_cards)
    #                     break
    #                 except:
    #                     pass
    #             if not game.check_valid(chosen_cards):  # if the cards chosen are not valid
    #                 print('[INVALID CARDS]')
    #                 queue.clear()
    #                 print('queue is:', queue)
    #                 turn_msg = "INVALID"
    #                 break
    #             else:
    #                 print('[VALID CARDS]')
    #                 game.going_out(chosen_cards)
    #                 for i in range(0, len(chosen_cards)):
    #                     print(chosen_cards)
    #                     print(all_cards[who_starts])
    #                     all_cards[who_starts].remove(int(chosen_cards[i]))
    #                     print(f"[UPDATED P1 CARDS] {all_cards[who_starts]}")
    #                 new_card = game.deal(1)
    #                 all_cards[who_starts].append(new_card[0])
    #                 turn_msg = f"VALID Your updated cards: {all_cards[who_starts]}"
    #                 current_players[who_starts].send(turn_msg.encode(FORMAT))
    #                 queue.clear()
    #                 turn = False
    #                 break
    #
    #     turn = True
    #     turn_msg = 'Its your turn!'
    #     while turn:
    #         while len(queue) == 0:
    #             place = 0
    #             if who_starts == 0:
    #                 current_players[who_starts + 1].send(turn_msg.encode(FORMAT))
    #                 place = who_starts + 1
    #             else:
    #                 current_players[who_starts - 1].send(turn_msg.encode(FORMAT))
    #                 place = who_starts - 1
    #             while True:
    #                 try:
    #                     chosen_cards = queue[0].split(' ')
    #                     time.sleep(1)
    #                     print("\nThe chosen cards: ", chosen_cards)
    #                     break
    #                 except:
    #                     pass
    #             if not game.check_valid(chosen_cards):  # if the cards chosen are not valid
    #                 print('[INVALID CARDS]')
    #                 queue.clear()
    #                 print('queue is:', queue)
    #                 turn_msg = "INVALID"
    #                 break
    #             else:
    #                 print('[VALID CARDS]')
    #                 game.going_out(chosen_cards)
    #                 for i in range(0, len(chosen_cards)):
    #                     print(who_starts)
    #                     print(place)
    #                     print(all_cards)
    #                     print(all_cards[place])
    #                     all_cards[place].remove(int(chosen_cards[i]))
    #
    #                     print(f"[UPDATED P1 CARDS] {all_cards[place]}")
    #                 new_card = game.deal(1)
    #                 all_cards[place].append(new_card[0])
    #                 turn_msg = f"VALID Your new card: {all_cards[place]}"
    #                 current_players[place].send(turn_msg.encode(FORMAT))
    #                 queue.clear()
    #                 turn = False
    #                 break




print("[STARTING] server is starting...")
start()
print("now what")
game(clients)

#game_between_two(clients[0], clients[1])
