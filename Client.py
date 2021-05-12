import socket
import threading
import time
from Yaniv import Yaniv
import stam
import pygame

PORT = 5050
FORMAT = 'utf-8'

DISCONNECT_MESSAGE = "!DISCONNECT"
INVALID = "INVALID"
VALID = "VALID"
NOT_YOU_YANIV_MESSAGE = 'NYYANIV'

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


msg_queue = []
session_queue = []

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# PYGAME VARS
WIDTH, HEIGHT = 1280, 720

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yaniv")

image = pygame.image.load('backtry.jpg')
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BORDO = (138, 25, 25)
FPS = 60

List_updates = []

pygame.init()
myfont_BIG = pygame.font.Font('myfont.ttf', int(WIDTH/4.26))
myfont_medium = pygame.font.Font('myfont.ttf', int(WIDTH/25.6))
myfont_small = pygame.font.Font('myfont.ttf', int(WIDTH/32))

soundObj = pygame.mixer.Sound('ElevatorMusic.wav')
ww_music = pygame.mixer.Sound('WildWestern.wav')

# GRAPHICS
def draw_wating_for_players():
    #WIN.blit(image, (0, 0))

    text = myfont_medium.render('Waiting for players', True, WHITE)
    text_1dot = myfont_medium.render('Waiting for players.', True, WHITE)
    text_2dot = myfont_medium.render('Waiting for players..', True, WHITE)
    text_3dot = myfont_medium.render('Waiting for players...', True, WHITE)


    #textRect = text.get_rect()
    #textRect.center = (WIDTH/2, HEIGHT/2)
    soundObj.play()
    y = HEIGHT
    while y > HEIGHT/2:
        WIN.blit(image, (0, 0))
        # textRect.center = (WIDTH/2, y)
        WIN.blit(text, (int(WIDTH/2.6), HEIGHT/2.3))
        pygame.display.update()

        y -= 1

    loop = True
    while loop:
        WIN.blit(image, (0, 0))
        pygame.display.update()


        WIN.blit(text, (int(WIDTH/2.6), HEIGHT/2.3))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(image, (0, 0))
        WIN.blit(text_1dot, (int(WIDTH/2.6), HEIGHT/2.3))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(image, (0, 0))
        WIN.blit(text_2dot, (int(WIDTH/2.6), HEIGHT/2.3))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(image, (0, 0))
        WIN.blit(text_3dot, (int(WIDTH/2.6), HEIGHT/2.3))
        pygame.display.update()
        time.sleep(0.3)

        for mes in session_queue:
            if mes.split('&')[0] == 'SGC':
                soundObj.stop()
                return
def fade_in(object, pos, secs, other_objects):
    alpha = 0
    times = 0
    cl = pygame.time.Clock()
    while alpha < 256:
        for objects in other_objects:
            WIN.blit(objects[0], objects[1])
        cl.tick(25)
        time.sleep(0.04)
        times += 0.04
        object.set_alpha(alpha)
        WIN.blit(object, pos)
        pygame.display.update()
        alpha += 5
        if times > secs:
            object.set_alpha(255)
            WIN.blit(object, pos)
            pygame.display.update()
            print("end fade")
            return
def draw_opensc():
    true = True
    while true:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                true = False
    #ww_music.play()
    WIN.blit(image, (0, 0))


    wlc = myfont_small.render('Welcome to:', True, WHITE)
    WIN.blit(wlc, (WIDTH/12, HEIGHT/4))
    #fade_in(wlc, (WIDTH/12, HEIGHT/4), 2, [[image, (0, 0)]])

    #objects = [[image, (0, 0)], [wlc, (WIDTH/12, HEIGHT/4)]]
    text = myfont_BIG.render('Yaniv', True, WHITE)

    #fade_in(text, pos, 4, objects)
    #objects.append([text, pos])

    pos = (int(WIDTH/13), HEIGHT/3.3)
    WIN.blit(text, pos)

    bg = pygame.image.load('cards_bg.png')
    bg = pygame.transform.scale(bg, (int(WIDTH/2.5), int(HEIGHT/1.4234)))
    #print(f'imageW {bg.get_width()} and imageH {bg.get_height()}')

    #fade_in(bg, (WIDTH/2, HEIGHT/7), 2, objects)
    WIN.blit(bg, (WIDTH/2, HEIGHT/7))

    #pygame.display.update()
    time.sleep(0.4)
    by = myfont_medium.render('By: Adam Kol', True, WHITE)
    x = -WIDTH/5
    power = WIDTH/12.8
    WIN.blit(by, (x, HEIGHT/1.6))
    pygame.display.update()
    while x < WIDTH/3.5:
        x += power/2
        power = power/1.1 + 1
        WIN.blit(image, (0, 0))
        WIN.blit(text, (int(WIDTH/13), HEIGHT/3.3))
        WIN.blit(wlc, (WIDTH/12, HEIGHT/4))
        WIN.blit(bg, (WIDTH/2, HEIGHT/7))

        WIN.blit(by, (x, HEIGHT/1.6))

        pygame.display.update()

    time.sleep(1.5)
    any = myfont_small.render('PRESS ANY KEY TO CONTINUE', True, WHITE)
    # any.set_alpha(255)
    textRect = any.get_rect()
    textRect.center = (WIDTH/2, HEIGHT/1.1)
    #WIN.blit(any, textRect)
    #pygame.display.update()

    alpha = 0
    down = True
    while True:

        WIN.blit(image, (0, 0))
        WIN.blit(text, (int(WIDTH/13), HEIGHT/3.3))
        WIN.blit(wlc, (WIDTH/12, HEIGHT/4))
        WIN.blit(bg, (WIDTH/2, HEIGHT/7))
        WIN.blit(by, (x, HEIGHT/1.6))

        if alpha > 0 and down:
            alpha -= 1

        elif alpha == 0:
            down = False
            alpha += 1

        elif alpha < 255 and not down:
            alpha += 1

        elif alpha == 255:
            down = True
            alpha -= 1

        any.set_alpha(alpha)
        WIN.blit(any, textRect)
        pygame.display.update()
        #
        # #time.sleep(0.7)
        #
        # WIN.blit(any, textRect)
        # pygame.display.update()

        #time.sleep(0.7)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #ww_music.stop()
                return
def draw_cards(cards):

    cards_num = len(cards)
    ratio = 5
    dif = WIDTH/9
    if cards_num > 4:
        dif = WIDTH/18
    i = WIDTH/2 - 0.5*(cards_num - 1)*dif
    for item in cards:
        card = fr'PNG\{item}.png'
        card_image = pygame.image.load(card)


        card_w = 691/ratio
        card_h = 1056/ratio


        card_image = pygame.transform.scale(card_image, (int(card_w), int(card_h)))

        #print(f'imageW {image.get_width()} and imageH {image.get_height()}')

        card_rect = card_image.get_rect()
        card_rect.center = (i, HEIGHT - HEIGHT/5)

        WIN.blit(card_image, card_rect)
        pygame.display.update()

        i += dif
    return (691/ratio, 1056/ratio)


def message():
    if len(session_queue) != 0:
        res = session_queue[0]
        session_queue.remove(res)
        return res
    return False

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


def match(client):
    print("[MATCH THREAD STARTED]")
    cards = wait_for_msg(header='SGC')[:-1]
    #time.sleep(1)
    session_queue.append(f'SGC&{cards}')  # SESSION QUEUE
    print("[YOUR CARDS ARE]", cards)

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
            print(f"Your new cards are: {new_cards}")

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

def main():
    draw_opensc()  # stops when a key pressed

    session_thread = threading.Thread(target=match, args=(client, ))
    session_thread.start()

    draw_wating_for_players()  # stops when got cards

    WIN.blit(image, (0, 0))
    pygame.display.update()
    print("draw finished")

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        mes = message()
        print("Gmes:", mes)
        if mes.split('&')[0] == 'SGC':
            cards = mes.split('&')[1].split(' ')
            print("Gcards:", cards)
            draw_cards(cards)


    #res = match(client)
    if session_thread == 'MBW':
        end_res = wait_for_msg(header='EM')
        print(end_res)

start_thread(client)
main()
