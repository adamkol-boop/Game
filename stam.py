import pygame
import threading
import time
WIDTH, HEIGHT = 1280, 720

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yaniv")

image = pygame.image.load('backro.jpg')
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
FPS = 60

def draw_window():
    WIN.blit(image, (0, 0))
    pygame.display.update()



pygame.init()
myfont_BIG = pygame.font.Font('myfont.ttf', int(WIDTH/4.26))
myfont_medium = pygame.font.Font('myfont.ttf', int(WIDTH/25.6))
myfont_small = pygame.font.Font('myfont.ttf', int(WIDTH/32))




def draw_opensc():
    WIN.blit(image, (0, 0))

    text = myfont_BIG.render('Yaniv', True, WHITE)
    #textRect = text.get_rect()
    #textRect.center = (WIDTH/4, HEIGHT/3.5)
    WIN.blit(text, (int(WIDTH/13), HEIGHT/3.3))

    wlc = myfont_small.render('Welcome to:', True, WHITE)
    WIN.blit(wlc, (WIDTH/12, HEIGHT/4))

    bg = pygame.image.load('cards_bg.png')
    bg = pygame.transform.scale(bg, (int(WIDTH/2.5), int(HEIGHT/1.4234)))
    print(f'imageW {bg.get_width()} and imageH {bg.get_height()}')
    WIN.blit(bg, (WIDTH/2, HEIGHT/7))

    pygame.display.update()
    time.sleep(3)
    by = myfont_medium.render('By: Adam Kol', True, WHITE)
    x = -WIDTH/5
    power = WIDTH/12.8
    WIN.blit(by, (x, HEIGHT/1.6))
    pygame.display.update()
    while x < WIDTH/3.5:
        WIN.blit(image, (0, 0))
        WIN.blit(text, (int(WIDTH/13), HEIGHT/3.3))
        WIN.blit(wlc, (WIDTH/12, HEIGHT/4))
        WIN.blit(bg, (WIDTH/2, HEIGHT/7))

        WIN.blit(by, (x, HEIGHT/1.6))
        x += power/2
        power = power/1.1 + 1
        pygame.display.update()

    time.sleep(1.5)
    any = myfont_small.render('PRESS ANY KEY TO CONTINUE...', True, WHITE)
    textRect = any.get_rect()
    textRect.center = (WIDTH/2, HEIGHT/1.1)
    WIN.blit(any, textRect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

ratio = 0
def draw_cards(cards, mx, my):
    cards_num = len(cards)
    ratio = 5
    dif = WIDTH/9
    if cards_num > 4:
        dif = WIDTH/18
    i = WIDTH/2 - 0.5*(cards_num - 1)*dif
    for item in cards:
        card = fr'PNG\{item}.png'
        image = pygame.image.load(card)


        card_w = 691/ratio
        card_h = 1056/ratio


        image = pygame.transform.scale(image, (int(card_w), int(card_h)))

        #print(f'imageW {image.get_width()} and imageH {image.get_height()}')

        card_rect = image.get_rect()
        card_rect.center = (i, HEIGHT - HEIGHT/5)

        WIN.blit(image, card_rect)
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
    run = True
    draw_opensc()
    print("draw finished")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        cards = [26, 53, 5, 6]

        #mx, my = pygame.mouse.get_pos()
        #size = draw_cards(cards, mx, my)

        #choosable(len(cards), size)
        #mx, my = pygame.mouse.get_pos()
        #print(f'x: {mx}, y: {my}')


    pygame.quit()




main()
