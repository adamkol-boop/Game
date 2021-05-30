import socket
import threading
import CardsMath as cm
import pygame
import stam as gc  # graphic class
import time

PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
INVALID = "INVALID"
VALID = "VALID"
NOT_YOU_YANIV_MESSAGE = 'NYYANIV'
YANIV_MESSAGE = 'yaniv'
# YANIV_MESSAGE = 'yaniv'

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

msg_queue = []

graphic_queue = []
graphic_respond_queue = []

names = []
number_of_players = -1
client_index = -1

def handle_msg(client):
    global number_of_players
    print('[THREAD IS ON]')

    connected = True
    while connected:
        data = client.recv(1024).decode(FORMAT)
        if data == DISCONNECT_MESSAGE:
            connected = False

        if data.split('&')[0] == 'BROADCAST':  # means got broadcast
            header = data.split('&')[1]
            if header == 'WFP':  # waiting for players
                content = data.split('&')[2]
                number_connected = content.split('$')[0]
                new_name = content.split('$')[1]
                print("got number in lobby", number_connected)
                print("got nre name", new_name)
                time.sleep(1)
                gc.draw_number_in_lobby(number_connected)
                number_of_players = number_connected
            if header == 'RS':
                time.sleep(1)
                gc.draw_stack(5)
            if header == 'ULC':  # Updated last cards
                time.sleep(1)
                content = data.split('&')[2]
                graphic_queue.append(f'{header}%{content}')
                #gc.used_cards(data.split('&')[2].split(' '))
            if header == 'PCY':  # player called Yaniv
                print("got broadcast PCY")
                time.sleep(1)
                all_cards = data.split('&')[2]
                graphic_queue.append(f'{header}%{all_cards}')
        msg_queue.append(data)


def wait_for_msg(header):
    '''headers possible:
    LC = last cards
    TM = turn message
    SGC = start game cards
    NC = new cards
    EML = end message loose
    EMA = end message asaf
    CC = chosen cards
    '''
    while True:
        while len(msg_queue) == 0:
            pass
        i = -1
        for item in msg_queue:
            i += 1
            if item.split('&')[0] == header:
                msg = msg_queue[i]
                msg_queue.remove(msg)

                msg = msg.split('&')[1:]
                # print('msg-->', msg)
                return msg[0]
            # if item.split('&')[0] == 'BROADCAST':
            #     #print(item.split('&')[1])
            #     msg = msg_queue[i]
            #     msg_queue.remove(msg)
            #     if item.split('&')[1] == 'ULC':
            #         # means someone finished his turn
            #         #print(item.split('&'))
            #         content = item.split('&')[2]
            #         print("broadcast mes is:", content)
            #         graphic_queue.append(f'ULC%{content}')  # draws the cards
            #         return
            #     if item.split('&')[1] == 'AS':
            #         content = item.split('&')[2]
            #         print("broadcast mes is:", content)
            #         graphic_queue.append(f'AS%{content}')  # draws the cards


def start_thread(client):
    thread = threading.Thread(target=handle_msg, args=(client, ))
    thread.start()

def organize_list(list, player_index):
    '''
    the function organizes the ordre of the card sums of the other players
    :param sums: all sums of cards (including the client -> getting it from server)
    :param player_index: the index of the player in the array (tells which sum is his)
    :return: list of the sums to drae by clock order
    '''
    print('-------------------------\n')
    print("PLAYER INDEX IS", player_index)
    print("sums in funciton are", list)
    print("number of players", number_of_players)
    res = []
    if player_index == 0:
        for i in range(1, len(list)):
            res.append(list[i])
            print('appended with 0')
    elif player_index == int(number_of_players) - 1: # if he is the last player
        for i in range(0, len(list) - 1):
            res.append(list[i])
            print("appended")
    else:
        for i in range(player_index + 1, len(list)):
            res.append(list[i])
        for i in range(0, player_index):
            res.append(list[i])

    print('-------------------------\n')
    return res

def graphics():

    print("entered the graphics thread")

    run = True
    #WIN.blit(gc.blue_backg, (0, 0))
    pygame.display.update()
    #global all_names
    printed_screen = False
    while run:
        #print(graphic_queue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        #print(graphic_queue)
        for graphic in graphic_queue:
            header = graphic.split('%')[0]
            print("header is", header)

            if header == 'SGC':
                content = graphic.split('%')[1]
                print("got the draw cards message")
                print("content before split:", content)

                cards = content.split('$')[0].split(' ')
                #all_names = content.split('$')[1].split(' ')

                #names_needed = organize_list(all_names, client_index)

                print("cards:", cards, "len:", len(content))
                sums = []
                for i in range(0, int(number_of_players) - 1):
                    sums.append(5)
                print(cards)
                gc.draw_back_to_game(sums, 5, names)
                #gc.draw_all_names(names_needed)
                print("names PRINTEDDDDDDDD")
                #gc.draw_cards(content, [], [], [-1], [])
                printed_screen = True
                graphic_queue.remove(graphic)

            if header == 'ULC':
                if printed_screen:
                    last_cards = graphic.split('%')[1].split('$')[0].split(' ')
                    all_players_sums = graphic.split('%')[1].split('$')[1].split(' ')
                    print('all sums are', all_players_sums)
                    sums = organize_list(all_players_sums, client_index)
                    print("clients sum is:", sums)
                    gc.draw_enemy_cards(sums, names)
                    graphic_queue.remove(graphic)
                    print("got the ULC message")
                    print("last cards before split:", last_cards)

                    gc.used_cards(last_cards)

            if header == 'PCY':
                print("should print th yaniv message")
                all_cards = graphic.split('%')[1]
                graphic_queue.remove(graphic)
                graphic_respond_queue.append(f'PCY%{all_cards}')
                #gc.when_called_yaniv('Adam', all_cards)


def list_to_string(card_list):
    p_cards_str = ''
    for card in card_list[:-1]:
        p_cards_str += str(card) + ' '
    p_cards_str += str(card_list[-1])
    return p_cards_str


def match(client, name):
    '''the function gets the connection socket with the server
    and handles the gaem itself. all the logic is going here.
    void function'''
    sums = []
    global client_index
    global names
    for i in range(0, int(number_of_players) - 1):
        sums.append(5)

    print('waiting for sgc now')
    cards_n_names = wait_for_msg(header='SGC')
    print('sgc received:', cards_n_names)

    new_cards_string = cards_n_names.split('$')[0]
    all_names = cards_n_names.split('$')[1].split(' ')


    print('got all names with sgc', all_names)
    client_index = all_names.index(name)
    names = organize_list(all_names, client_index)

    print("new cards string is:", new_cards_string)
    #names_needed = organize_list(all_names, client_index)
    graphic_queue.append(f'SGC%{new_cards_string}')  # the draw thread is drawing: background, enemy cards, your cards.

    print("[YOUR CARDS ARE]", new_cards_string)

    new_cards = new_cards_string.split(' ')
    gc.draw_cards(new_cards, [], [], [-1], [])


    game_is_on = True
    while game_is_on:
        '''the message below is the begining of every turn.
        three options for messages here:
        1 = LC --> a regular turn
        2 = EML --> game has ended, you are the looser
        3 = EMA --> game has ended, you are the winner with an asaf'''

        last_cards = wait_for_msg(header='LC') # waiting for last cards


        if last_cards == 'EML':  # end message loose. final
            #graphic_queue.append('EML')  # added
            stop = False
            while not stop:
                for item in graphic_respond_queue:
                    header = item.split('%')[0]
                    if header == 'PCY':
                        print('GOT THE HEADER PCY FROM THE GRAPHIC RESPOND')
                        all_cards = item.split('%')[1]
                        graphic_respond_queue.remove(item)
                        gc.when_called_yaniv('Someone', new_cards_string, all_cards)
                        stop = True
                    pygame.display.flip()
            print('[BETTER LUCK NEXT TIME...]')
            return False
        if last_cards == 'EMA':
            #graphic_queue.append('EMA')  # added
            print('[OMG SHEEESHHHHH YOU GOT AN ASAF!]') # end message assaf. final
            return False

        last_cards = last_cards.split(' ')
        #graphic_queue.append(f'LC%{last_cards}')  # last cards --> used_cards()
        print(f'[THE LAST CARDS] {last_cards}')
        print("It's your turn!")
        res = gc.choose(new_cards, last_cards)
        if res[0] == YANIV_MESSAGE:
            client.send(f'CC&VY'.encode(FORMAT))  # chosen cards --> valid message

            stop = False
            while not stop:
                for item in graphic_respond_queue:
                    header = item.split('%')[0]
                    if header == 'PCY':
                        print('GOT THE HEADER PCY FROM THE GRAPHIC RESPOND')
                        all_cards = item.split('%')[1]
                        graphic_respond_queue.remove(item)
                        gc.when_called_yaniv(name, new_cards_string, all_cards)
                        stop = True

            print('fuckin yaniv')
            return "match ended"

        # --------------------------------------------------
        else:
            chosen = list_to_string(res[1])
            client.send(f'CC&{chosen}'.encode(FORMAT))  # already valid
            print('[CARDS SENT]', chosen)
            time.sleep(0.5)
            if res[0] == 'DECK':
                client.send(f'DL&{res[0]}'.encode(FORMAT))
            elif res[0] == 'LAST':
                client.send(f'DL&{res[0]}&{res[-1][-1]}'.encode(FORMAT))
                last_cards.remove(res[-1][-1])

            # print("res is", int(res[-1][-1]))
            # print("last cards:", last_cards)
            #gc.draw_cards
            gc.draw_back_to_game(sums, 5, names)
            #names_orgsd = organize_list(all_names, client_index)  # names organized
            #gc.draw_all_names(names_orgsd)
            print("turn done")

            #------------------------------------------------------

        #graphic_queue.append(f'CH')  # ch stands for choose

        # now wait for chosen cards
        #while len(graphic_respond_queue) == 0:
            #pass

        # is_valid = False
        # while not is_valid:
        #     chosen_cards  = input("[CHOOSE YOUR CARDS] ")
        #
        #
        #     if chosen_cards.upper() == 'YANIV':
        #         cards_sum = cm.sum_cards(new_cards)
        #         if cards_sum < 7:
        #             client.send(f'CC&VY&{new_cards}'.encode(FORMAT))  # valid yaniv
        #             return True
        #     else:
        #         #print("the chosen cards are:", chosen_cards.split(' '))
        #         is_valid = cm.check_valid(chosen_cards.split(' '))  # if it returns true so turn is valid
        #         if not is_valid:
        #             print("[INVALID CARDS]")

            # if the code is here it means the turn is valid or its a valid yaniv
        #---------------------------------
        # chosen = list_to_string(res[1])
        # client.send(f'CC&{chosen}'.encode(FORMAT))  # already valid
        # print('[CARDS SENT]', chosen)
        #
        # time.sleep(0.5)
        # if res[0] == 'DECK':
        #     client.send(f'DL&{res[0]}'.encode(FORMAT))
        # elif res[0] == 'LAST':
        #     client.send(f'DL&{res[0]}&{res[-1][-1]}'.encode(FORMAT))

        # deck_or_last = input('choose L for last or D for deck ')
        # if deck_or_last.lower() == 'l':
        #     print('len of last cards', len(last_cards), last_cards)
        #     if len(last_cards) == 1:
        #         client.send(f'DL&LAST&{last_cards[0]}'.encode(FORMAT))
        #     else:
        #         what_cards = input("[CHOOSE THE CARD YOU WANT TO KEEP]")
        #         while not (int(what_cards) == int(last_cards[0]) or int(what_cards) == int(last_cards[-1])):
        #             what_cards = input("[CHOOSE AGAIN THE CARD YOU WANT TO KEEP]")
        #         client.send(f'DL&LAST&{what_cards}'.encode(FORMAT))  # deck/last
        # if deck_or_last.lower() == 'd':
        #     client.send('DL&DECK&chose deck'.encode(FORMAT)) # deck/last

        new_cards_string = wait_for_msg(header='NC')  # waiting for new cards
        new_cards = new_cards_string.split(' ')
        print('new cards are:', new_cards)
        gc.draw_cards(new_cards, [], [], [-1], [])
        print(f"[YOUR NEW CARDS ARE] {new_cards}")
        print("[NEXT PLAYER NOW]\n")

def main():
    #  main
    #gc.draw_opensc()  # drawing open screen before the connection
    name = gc.get_name()  # getting the name
    print("name is", name)
    #name = "fuck"

    # now, the connection should be established
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    start_thread(client)  # handling messages started

    client.send(f'PN&{name}'.encode(FORMAT)) # players name

    gc.draw_wating_for_players()  # waiting until all the connections made

    print('finished waiting for clients')
    # now, before the game mechanics start, the graphic thread can start too
    graphic_thread = threading.Thread(target=graphics)
    graphic_thread.start()

    print("match is starting now")
    res = match(client, name[:-1])  # match
    print(res)
    if res:
        end_res = wait_for_msg(header='EM')
        print(end_res)

if __name__ == '__main__':
    main()
