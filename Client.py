import socket
import threading
import time
from Yaniv import Yaniv



PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
INVALID = "INVALID"
VALID = "VALID"
NOT_YOU_YANIV_MESSAGE = 'NYYANIV'

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


msg_queue = []


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    #msg_length = len(message)
    #send_length = str(msg_length).encode(FORMAT)
    #send_length += b' ' * (HEADER - len(send_length))
    #client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


#opponents_name = input("Your Name: ")
#send("Client 1")
def handle_msg(client):
    print('[THREAD IS ON]')

    connected = True
    while connected:
        data = client.recv(1024).decode(FORMAT)
        if data == DISCONNECT_MESSAGE:
            connected = False
        msg_queue.append(data)
        #print("[THE QUEUE IS NOW] ", msg_queue)


def wait_for_msg(header):
    '''headers possible:
    LC = last cards
    TM = turn message
    SGC = start game cards
    NC = new cards
    EML = end message loose
    EMA = end message asaf
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
                print(item.split('&')[1])
                msg = msg_queue[i]
                msg_queue.remove(msg)


def start_thread(client):
    thread = threading.Thread(target=handle_msg, args=(client, ))
    thread.start()

start_thread(client)

cards = wait_for_msg(header='SGC')[:-1]
#time.sleep(1)
print("[YOUR CARDS ARE]", cards)


def match(client):
    game_is_on = True
    while game_is_on:

        last_cards = wait_for_msg(header='LC') # waiting for last cards
        if last_cards == 'EML':
            print('[BETTER LUCK NEXT TIME...]')
            return
        if last_cards == 'EMA':
            print('[OMG SHEEESHHHHH YOU GOT AN ASAF!]')
            return
        print(f'[THE LAST CARDS] {last_cards}')

        turn = wait_for_msg(header='TM')  # waiting for turn message
        print("[MES IS]", turn)

        if turn == NOT_YOU_YANIV_MESSAGE:
            print("[OH NO SOMEONE CALLED YANIV...]")
            return

        # last_cards = wait_for_msg()
        # msg_queue.clear()
        # print(last_cards)

        while turn != VALID:
            chosen_cards  = input("[CHOOSE YOUR CARDS] ")
            client.send(chosen_cards.encode(FORMAT))
            print("[DATA SENT]")

            turn = wait_for_msg(header='TM')  # waiting for turn message
            print("[MES IS]", turn)

            if turn == 'VALID YANIV':
                print("[YOU MAY BE THE WINNER]")
                return 'MBW'  # may be winner
        #time.sleep(1)
        # last_cards = wait_for_msg()
        # msg_queue.clear()
        # print(last_cards)

        deck_or_last = input("[CHOOSE D FOR DECK L FOR LAST] ")
        if deck_or_last.lower() == 'd':
            client.send('DECK'.encode(FORMAT))
            print("[YOU CHOSE DECK]")

            new_cards = wait_for_msg(header='NC')  # waiting for new cards
            print(new_cards)

        elif deck_or_last.lower() == 'l':
            client.send('LAST'.encode(FORMAT))
            #last_cards = wait_for_msg()
            #msg_queue.clear()

            #print(last_cards)
            chosen = input("[WHICH CARD YOU WANT TO KEEP] ")
            client.send(chosen.encode(FORMAT))

            new_cards = wait_for_msg(header='NC')  # waiting for new cards
            print(new_cards)

        print("[NEXT PLAYER NOW]\n")


res = match(client)
if res == 'MBW':
    end_res = wait_for_msg(header='EM')
    print(end_res)
