import socket
import threading
import CardsMath as cm

PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
INVALID = "INVALID"
VALID = "VALID"
NOT_YOU_YANIV_MESSAGE = 'NYYANIV'
YANIV_MESSAGE = 'yaniv'

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

msg_queue = []

graphic_queue = []
graphic_respond_queue = []

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def handle_msg(client):
    print('[THREAD IS ON]')

    connected = True
    while connected:
        data = client.recv(1024).decode(FORMAT)
        if data == DISCONNECT_MESSAGE:
            connected = False
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
            if item.split('&')[0] == 'BROADCAST':
                #print(item.split('&')[1])
                msg = msg_queue[i]
                msg_queue.remove(msg)
                if item.split('&')[1] == 'ULC':
                    # means someone finished his turn
                    #print(item.split('&'))
                    content = item.split('&')[2]
                    print("broadcast mes is:", content)
                    graphic_queue.append(f'ULC%{content}')  # draws the cards
                if item.split('&')[1] == 'AS':
                    content = item.split('&')[2]
                    print("broadcast mes is:", content)
                    graphic_queue.append(f'AS%{content}')  # draws the cards


def start_thread(client):
    thread = threading.Thread(target=handle_msg, args=(client, ))
    thread.start()

start_thread(client)

def match(client):
    '''the function gets the connection socket with the server
    and handles the gaem itself. all the logic is going here.
    void function'''
    cards = wait_for_msg(header='SGC').split(' ')
    #graphic_queue.append(f'SGC%{cards}')  # adding
    print("[YOUR CARDS ARE]", cards)

    new_cards = cards
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

        #graphic_queue.append(f'CH')  # ch stands for choose

        # now wait for chosen cards
        #while len(graphic_respond_queue) == 0:
            #pass

        is_valid = False
        while not is_valid:
            chosen_cards  = input("[CHOOSE YOUR CARDS] ")


            if chosen_cards.upper() == 'YANIV':
                cards_sum = cm.sum_cards(new_cards)
                if cards_sum < 7:
                    client.send(f'CC&VY&{new_cards}'.encode(FORMAT))  # valid yaniv
                    return True
            else:
                #print("the chosen cards are:", chosen_cards.split(' '))
                is_valid = cm.check_valid(chosen_cards.split(' '))  # if it returns true so turn is valid
                if not is_valid:
                    print("[INVALID CARDS]")

            # if the code is here it means the turn is valid or its a valid yaniv
        client.send(f'CC&{chosen_cards}'.encode(FORMAT))  # already valid
        print('[CARDS SENT]')

        deck_or_last = input('choose L for last or D for deck ')
        if deck_or_last.lower() == 'l':
            print('len of last cards', len(last_cards), last_cards)
            if len(last_cards) == 1:
                client.send(f'DL&LAST&{last_cards[0]}'.encode(FORMAT))
            else:
                what_cards = input("[CHOOSE THE CARD YOU WANT TO KEEP]")
                while not (int(what_cards) == int(last_cards[0]) or int(what_cards) == int(last_cards[-1])):
                    what_cards = input("[CHOOSE AGAIN THE CARD YOU WANT TO KEEP]")
                client.send(f'DL&LAST&{what_cards}'.encode(FORMAT))  # deck/last
        if deck_or_last.lower() == 'd':
            client.send('DL&DECK&chose deck'.encode(FORMAT)) # deck/last

        new_cards = wait_for_msg(header='NC').split(' ')  # waiting for new cards
        print(f"[YOUR NEW CARDS ARE] {new_cards}")
        print("[NEXT PLAYER NOW]\n")


res = match(client)
if res:
    end_res = wait_for_msg(header='EM')
    print(end_res)
