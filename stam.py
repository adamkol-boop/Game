import pygame
import threading
import time
WIDTH, HEIGHT = 1280, 720

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yaniv")

image = pygame.image.load('backtry.jpg')
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)

FPS = 60

def draw_window():
    WIN.blit(image, (0, 0))
    pygame.display.update()

# List_updates = []

pygame.init()
myfont_BIG = pygame.font.Font('myfont.ttf', int(WIDTH/4.26))
myfont_medium = pygame.font.Font('myfont.ttf', int(WIDTH/25.6))
myfont_small = pygame.font.Font('myfont.ttf', int(WIDTH/32))

soundObj = pygame.mixer.Sound('ElevatorMusic.wav')
ww_music = pygame.mixer.Sound('WildWestern.wav')



def draw_opensc():
    true = True
    while true:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                true = False
    ww_music.play()
    WIN.blit(image, (0, 0))


    wlc = myfont_small.render('Welcome to:', True, WHITE)
    #WIN.blit(wlc, (WIDTH/12, HEIGHT/4))
    fade_in(wlc, (WIDTH/12, HEIGHT/4), 2, [[image, (0, 0)]])

    objects = [[image, (0, 0)], [wlc, (WIDTH/12, HEIGHT/4)]]
    text = myfont_BIG.render('Yaniv', True, WHITE)
    #textRect = text.get_rect()
    #textRect.center = (WIDTH/4, HEIGHT/3.5)
    pos = (int(WIDTH/13), HEIGHT/3.3)
    fade_in(text, pos, 4, objects)
    objects.append([text, pos])
    #WIN.blit(text, (int(WIDTH/13), HEIGHT/3.3))



    bg = pygame.image.load('cards_bg.png')
    bg = pygame.transform.scale(bg, (int(WIDTH/2.5), int(HEIGHT/1.4234)))
    #print(f'imageW {bg.get_width()} and imageH {bg.get_height()}')

    fade_in(bg, (WIDTH/2, HEIGHT/7), 2, objects)
    #WIN.blit(bg, (WIDTH/2, HEIGHT/7))

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
                ww_music.stop()
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



def draw_enemy_cards(sums):
    '''the function gets a list of
    the cards amount of each player
    means the len is the players number'''
    back_card = 0
    if len(sums) == 1:
        pass



def draw_wating_for_players():
    #WIN.blit(image, (0, 0))

    text = myfont_medium.render('Waiting for players', True, BORDO)
    text_1dot = myfont_medium.render('Waiting for players.', True, BORDO)
    text_2dot = myfont_medium.render('Waiting for players..', True, BORDO)
    text_3dot = myfont_medium.render('Waiting for players...', True, BORDO)

    # text.set_alpha(140)
    # text_1dot.set_alpha(140)
    # text_2dot.set_alpha(140)
    # text_3dot.set_alpha(140)

    #textRect = text.get_rect()
    #textRect.center = (WIDTH/2, HEIGHT/2)
    soundObj.play()
    y = HEIGHT
    while y > HEIGHT/3:
        WIN.blit(image, (0, 0))
        # textRect.center = (WIDTH/2, y)
        WIN.blit(text, (int(WIDTH/2.5), y))
        pygame.display.update()

        y -= 1

    y += 1
    loop = True
    while loop:
        WIN.blit(image, (0, 0))
        pygame.display.update()


        WIN.blit(text, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(image, (0, 0))
        WIN.blit(text_1dot, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(image, (0, 0))
        WIN.blit(text_2dot, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(image, (0, 0))
        WIN.blit(text_3dot, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                soundObj.stop()
                loop = False


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


def choosable(cards_num, size):
    dif = WIDTH/9
    if cards_num > 4:
        dif = WIDTH/18

    oh = pygame.mouse.get_pressed(3)
    print(oh)


def main():
    clock = pygame.time.Clock()
    #thread = threading.Thread(target=check)
    #thread.start()
    draw_opensc()

    run = True
    draw_wating_for_players()
    WIN.blit(image, (0, 0))
    pygame.display.update()

    print("draw finished")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



        #print("draw finished")
        cards = [26, 53, 5, 6]
        draw_cards(cards)
        #match()
        #mx, my = pygame.mouse.get_pos()
        #size = draw_cards(cards, mx, my)

        #choosable(len(cards), size)
        #mx, my = pygame.mouse.get_pos()
        #print(f'x: {mx}, y: {my}')


    pygame.quit()



if __name__ == '__main__':
    main()
