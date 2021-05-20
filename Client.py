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
# YANIV_MESSAGE = 'yaniv'

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

msg_queue = []

graphic_queue = []
graphic_respond_queue = []
number_of_players = -1

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
                number_connected = data.split('&')[2]
                print("got number in lobby", number_connected)
                time.sleep(1)
                gc.draw_number_in_lobby(number_connected)
                number_of_players = number_connected
            if header == 'RS':
                time.sleep(1)
                gc.draw_stack(5)
            if header == 'ULC':
                time.sleep(1)
                last_cards = data.split('&')[2]
                graphic_queue.append(f'{header}%{last_cards}')
                #gc.used_cards(data.split('&')[2].split(' '))
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

def graphics():

    print("entered the graphics thread")

    run = True
    #WIN.blit(gc.blue_backg, (0, 0))
    pygame.display.update()

    printed_screen = False
    while run:
        #print(graphic_queue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for graphic in graphic_queue:
            header = graphic.split('%')[0]
            print("header is", header)

            if header == 'SGC':
                content = graphic.split('%')[1]
                print("got the draw cards message")
                print("content before split:", content)

                content = content.split(' ')
                print("cards:", content, "len:", len(content))
                sums = []
                for i in range(0, int(number_of_players) - 1):
                    sums.append(5)
                print(content)
                gc.draw_back_to_game(content, sums, 5, [])
                #gc.draw_cards(content, [], [], [-1], [])
                printed_screen = True
                graphic_queue.remove(graphic)

            if header == 'ULC':
                if printed_screen:
                    last_cards = graphic.split('%')[1].split(' ')
                    graphic_queue.remove(graphic)
                    print("got the ULC message")
                    print("last cards before split:", last_cards)

                    gc.used_cards(last_cards)


def list_to_string(card_list):
    p_cards_str = ''
    for card in card_list[:-1]:
        p_cards_str += str(card) + ' '
    p_cards_str += str(card_list[-1])
    return p_cards_str

def match(client):
    '''the function gets the connection socket with the server
    and handles the gaem itself. all the logic is going here.
    void function'''
    sums = []
    for i in range(0, int(number_of_players) - 1):
        sums.append(5)

    cards = wait_for_msg(header='SGC')
    graphic_queue.append(f'SGC%{cards}')  # the draw thread is drawing: background, enemy cards, your cards.

    print("[YOUR CARDS ARE]", cards)

    new_cards = cards.split(' ')
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
        gc.draw_back_to_game(res[-1], sums, 5, last_cards)
        print("turn done")
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

        new_cards = wait_for_msg(header='NC').split(' ')  # waiting for new cards
        print('new cards are:', new_cards)
        gc.draw_cards(new_cards, [], [], [-1], [])
        print(f"[YOUR NEW CARDS ARE] {new_cards}")
        print("[NEXT PLAYER NOW]\n")

def main():
    #  main
    #gc.draw_opensc()  # drawing open screen before the connection
    #name = gc.get_name()  # getting the name

    # now, the connection should be established
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    start_thread(client)  # handling messages started

    gc.draw_wating_for_players()  # waiting until all the connections made

    # now, before the game mechanics start, the graphic thread can start too
    graphic_thread = threading.Thread(target=graphics)
    graphic_thread.start()

    res = match(client)  # match
    if res:
        end_res = wait_for_msg(header='EM')
        print(end_res)

if __name__ == '__main__':
    main()
