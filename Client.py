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
IM_HOST = False
QUITTED = False
number_of_players = -1
client_index = -1

def handle_msg(client, my_name):
    global number_of_players
    global IM_HOST

    print('[THREAD IS ON]')

    connected = True
    while connected:
        data = client.recv(1024).decode(FORMAT)
        if QUITTED:
            return

        if data.split('&')[0] == 'BROADCAST':  # means got broadcast
            header = data.split('&')[1]
            if header == 'WFP':  # waiting for players
                content = data.split('&')[2]
                number_connected = content.split('$')[0]
                new_name = content.split('$')[1]
                host_name = content.split('$')[2]

                print(host_name, my_name[:-1])
                if host_name == my_name[:-1]:
                    IM_HOST = True
                    time.sleep(0.5)
                    gc.draw_number_in_lobby(number_connected, 'You are the host')
                    print('drawing host')
                else:
                    time.sleep(0.5)
                    gc.draw_number_in_lobby(number_connected, '{} is the host'.format(host_name))
                    print('drawing but not host')

                print("got number in lobby", number_connected)
                print("got nre name", new_name)
                time.sleep(1)


                print("number in lobby was drawn")
                number_of_players = number_connected
            if header == 'RS':
                time.sleep(1)
                gc.draw_stack(5)
            if header == 'ULC':  # Updated last cards
                time.sleep(1)
                content = data.split('&')[2]
                graphic_queue.append('{}%{}'.format(header, content))
                #gc.used_cards(data.split('&')[2].split(' '))
            if header == 'PCY':  # player called Yaniv
                print("got broadcast PCY")
                time.sleep(1)
                all_cards = data.split('&')[2].split('$')[0]
                winner_name = data.split('&')[2].split('$')[1]

                msg_queue.append('PCY&{}${}'.format(all_cards, winner_name))
        msg_queue.append(data)


def wait_for_msg(header):
    '''possible headers:
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
                return msg[0]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass



def start_thread(client, name):
    thread = threading.Thread(target=handle_msg, args=(client, name))
    thread.start()

def organize_list(list, player_index):
    '''
    the function organizes the ordre of the card sums of the other players
    :param sums: all sums of cards (including the client -> getting it from server)
    :param player_index: the index of the player in the array (tells which sum is his)
    :return: list of the sums to draw by clock order
    '''
    res = []
    if player_index == 0:  # its the first player, so the rest of the list...
        for i in range(1, len(list)):
            res.append(list[i])
            print('appended with 0')
    elif player_index == int(number_of_players) - 1: # if he is the last player, its all the places before
        for i in range(0, len(list) - 1):
            res.append(list[i])
            print("appended")
    else: # the places after, and then the places before
        for i in range(player_index + 1, len(list)):
            res.append(list[i])
        for i in range(0, player_index):
            res.append(list[i])

    return res

def graphics():
    global names
    run = True
    pygame.display.update()
    printed_screen = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for graphic in graphic_queue:
            header = graphic.split('%')[0]

            if header == 'SGC':
                content = graphic.split('%')[1]

                cards = content.split('$')[0].split(' ')
                sums = []
                for i in range(0, int(number_of_players) - 1):
                    sums.append(5)
                print(cards)
                gc.draw_back_to_game(sums, 5, names)
                printed_screen = True
                graphic_queue.remove(graphic)
            print('loop')
            if header == 'ULC':  # updated last cards
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

            if header == 'PCY':  # player called yaniv
                print("should print th yaniv message")
                all_cards = graphic.split('%')[1].split('$')[2]
                cards = graphic.split('%')[1].split('$')[1]
                winner_name = graphic.split('%')[1].split('$')[0]
                graphic_queue.remove(graphic)
                # graphic_respond_queue.append(f'PCY%{all_cards}')
                gc.when_called_yaniv(winner_name, cards, all_cards)

            if header == 'CC':  # choose cards
                graphic_queue.remove(graphic)
                cards = graphic.split('%')[1].split('$')[0]  # the cards split
                cards = cards.split(' ')
                last_cards = graphic.split('%')[1].split('$')[1]  # the last cards split
                last_cards = last_cards.split(' ')
                res = gc.choose(cards, last_cards)
                graphic_respond_queue.append(res)

            if header == 'BTG':  # back to game
                graphic_queue.remove(graphic)
                sums = graphic.split('%')[1].split('$')[0].split(' ')
                stack = graphic.split('%')[1].split('$')[1]
                names = graphic.split('%')[1].split('$')[2].split(' ')
                gc.draw_back_to_game(sums, stack, names)

            if header == 'DC':  # draw cards
                graphic_queue.remove(graphic)
                new_cards = graphic.split('%')[1]
                new_cards_list = new_cards.split(' ')
                print('new cards are', new_cards_list, len(new_cards_list))
                gc.draw_cards(new_cards_list, [], [], [-1], [])

            if header == 'OSC':  # open screen
                print('intro is going now')
                graphic_queue.remove(graphic)
                gc.draw_opensc()
                #name = gc.get_name()
                graphic_respond_queue.append('FINISH')

            if header == 'GN':  # get name
                print('taking name')
                graphic_queue.remove(graphic)
                name = gc.get_name()
                graphic_respond_queue.append('NAME%{}'.format(name))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pass
            if QUITTED:
                return

def list_to_string(card_list):
    p_cards_str = ''
    for card in card_list[:-1]:
        p_cards_str += str(card) + ' '
    p_cards_str += str(card_list[-1])
    return p_cards_str

def wait_for_graphic_res(header):
    '''
    the blocking function is waiting for a specific
    header to append in the graphic respond
    :param header: the header that is expected
    :return: the item
    '''
    print("waiting for graphics res")
    while True:
        for item in graphic_respond_queue:
            if item.split('%')[0] == header:
                res = item.split('%')[1]
                graphic_respond_queue.remove(item)
                return res


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

    client_index = all_names.index(name)
    names = organize_list(all_names, client_index)

    print("new cards string is:", new_cards_string)
    #names_needed = organize_list(all_names, client_index)
    graphic_queue.append('SGC%{}'.format(new_cards_string))  # the draw thread is drawing: background, enemy cards, your cards.
    time.sleep(0.5)
    print("[YOUR CARDS ARE]", new_cards_string)

    new_cards = new_cards_string.split(' ')
    graphic_queue.append('DC%{}'.format(new_cards_string))
    #gc.draw_cards(new_cards, [], [], [-1], [])


    game_is_on = True
    while game_is_on:
        '''the message below is the begining of every turn.
        three options for messages here:
        1 = LC --> a regular turn
        2 = EML --> game has ended, you are the looser
        3 = EMA --> game has ended, you are the winner with an asaf'''

        last_cards = wait_for_msg(header='LC') # waiting for last cards


        if last_cards == 'EML':  # end message loose. final

            print('waiting for pcy')
            all_cards_n_name = wait_for_msg('PCY')
            print('GOT THE HEADER PCY FROM THE GRAPHIC RESPOND', all_cards_n_name)
            all_cards = all_cards_n_name.split('$')[0]
            winner_name = all_cards_n_name.split('$')[1]
            #graphic_queue.append(f'PCY%{winner_name}${new_cards_string}${all_cards}')
            gc.when_called_yaniv(winner_name, new_cards_string, all_cards)
            print('[BETTER LUCK NEXT TIME...]')
            return False
        if last_cards == 'EMA':
            all_cards_n_name = wait_for_msg('PCY')
            all_cards = all_cards_n_name.split('$')[0]
            winner_name = all_cards_n_name.split('$')[1]
            gc.when_called_yaniv(winner_name, new_cards_string, all_cards)
            gc.when_assaf('wow! you just got an ASAF!')
            print('[YOU GOT AN ASAF!]') # end message assaf. final
            return False

        last_cards_list = last_cards.split(' ')
        #graphic_queue.append(f'LC%{last_cards}')  # last cards --> used_cards()
        #print(f'[THE LAST CARDS] {last_cards}')
        print("It's your turn!")
        #res = gc.choose(new_cards, last_cards)

        res = gc.choose(new_cards, last_cards_list)
        #graphic_queue.append(f'CC%{new_cards_string}${last_cards}')
        #res = wait_for_graphic_res('RES')
        if res[0] == YANIV_MESSAGE:
            client.send('CC&VY'.encode(FORMAT))  # chosen cards --> clients valid yaniv message

            print('waiting for pcy winner')
            yaniv_broadcast = wait_for_msg('PCY')
            all_cards = yaniv_broadcast.split('$')[0]
            gc.when_called_yaniv('You', new_cards_string, all_cards)
            #graphic_queue.append(f'PCY%You${new_cards_string}${all_cards}')
            return "match ended"

        # --------------------------------------------------
        else:
            chosen = list_to_string(res[1])
            client.send('CC&{}'.format(chosen).encode(FORMAT))  # already valid
            print('[CARDS SENT]', chosen)
            time.sleep(0.5)
            if res[0] == 'DECK':
                client.send('DL&{}'.format(res[0]).encode(FORMAT))
            elif res[0] == 'LAST':
                client.send('DL&{}&{}'.format(res[0], res[-1][-1]).encode(FORMAT))
                last_cards_list.remove(res[-1][-1])

            sums_str = list_to_string(sums)
            names_str = list_to_string(names)
            graphic_queue.append('BTG%{}$5${}'.format(sums_str, names_str))  # back to game
            #gc.draw_back_to_game(sums, 5, names)

        new_cards_string = wait_for_msg(header='NC')  # waiting for new cards
        new_cards = new_cards_string.split(' ')
        print('new cards are:', new_cards)
        graphic_queue.append('DC%{}'.format(new_cards_string))
        #gc.draw_cards(new_cards, [], [], [-1], [])
        print(f"[YOUR NEW CARDS ARE] {new_cards}")
        print("[NEXT PLAYER NOW]\n")

def if_quit(client):
    print('thread started now if quit')
    global QUITTED
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print('key pressed from if quit ')
                if event.key == pygame.K_ESCAPE:
                    print('key pressed from if quit its escape')
                    client.send(DISCONNECT_MESSAGE.encode(FORMAT))
                    QUITTED = True
                    return

GOT_NAME = False
def main():
    global GOT_NAME
    global MY_NAME
    #graphic_queue.append('OSC')
    #wait_for_graphic_res('FINISH')

    #graphic_queue.append('GN')
    #print("intro command sent")
    if GOT_NAME:
        gc.draw_opensc()  # drawing open screen before the connection
        GOT_NAME = True
    MY_NAME = gc.get_name()  # getting the name
    GOT_NAME = True

    graphic_thread = threading.Thread(target=graphics)
    graphic_thread.start()

    waiting_thread = threading.Thread(target=gc.draw_wating_for_players)
    waiting_thread.start()
    time.sleep(1)
    #name = wait_for_graphic_res('NAME')
    print("name is", MY_NAME)
    #name = "fuck"

    # now, the connection should be established
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # quit_thread = threading.Thread(target=if_quit, args=(client,))
    # quit_thread.start()

    start_thread(client, MY_NAME)  # handling messages started

    client.send('PN&{}'.format(MY_NAME).encode(FORMAT)) # players name
    time.sleep(0.5)

    print('thread for waiting for players started')

    if not IM_HOST:
        print('IM not the host')
        wait_for_msg('GIO')  # game is on
        gc.IS_STOP = True
    elif IM_HOST:
        print('IM the host')
        stop = False
        while not stop:
            #print('waiting for host to start')
            for event in pygame.event.get():
                print('searching events')
                if event.type == pygame.KEYDOWN:
                    print('key pressed')
                    if event.key == pygame.K_RETURN:
                        if int(number_of_players) > 1:
                            gc.IS_STOP = True
                            print('host pressed enter')
                            client.send('GIO&start'.encode(FORMAT))
                            time.sleep(0.2)
                            wait_for_msg('GIO')
                            stop = True
                        else:
                            pass
                    else:
                        pass

    print('finished waiting for clients')
    # now, before the game mechanics start, the graphic thread can start too

    time.sleep(0.2)
    print("match is starting now")
    res = match(client, MY_NAME[:-1])  # match
    print(res)
    if res:
        end_res = wait_for_msg(header='EM')
        gc.when_assaf(end_res)
        print(end_res)
    print('AND THATS IT')
    client.send(DISCONNECT_MESSAGE.encode(FORMAT))
    main()

if __name__ == '__main__':
    main()
