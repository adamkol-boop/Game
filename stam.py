import pygame
import threading
import time
import random
import CardsMath as cm


#---------------------------CONSTANTS--------------------------------------

WIDTH, HEIGHT = 1280, 720

YANIV_MESSAGE = 'yaniv'

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yaniv")

#-------<COLORS>---------
WHITE = (255, 255, 255)
BORDO = (138, 25, 25)

#-------<FONTS>----------
pygame.init()
myfont_BIG = pygame.font.Font('myfont.ttf', int(WIDTH/4.26))
myfont_medium_plus = pygame.font.Font('myfont.ttf', int(WIDTH/15))
myfont_medium = pygame.font.Font('myfont.ttf', int(WIDTH/25.6))
myfont_small = pygame.font.Font('myfont.ttf', int(WIDTH/32))

#--------<IMAGES>--------
intro_backg = pygame.image.load('backtry.jpg')  # wild west backround picture
intro_backg = pygame.transform.scale(intro_backg, (WIDTH, HEIGHT))

blue_backg = pygame.image.load('backro.jpg')  # second background, blue
blue_backg = pygame.transform.scale(blue_backg, (WIDTH, HEIGHT))

yaniv_crop = pygame.image.load(rf'PNG\yaniv_crop.png')  # the INTRO_BACKG cropped for the yaniv text
yaniv_crop = pygame.transform.scale(yaniv_crop, (WIDTH, HEIGHT))

by_adam_crop = pygame.image.load(rf'PNG\by_adam_crop.png')  # the INTRO_BACKG cropped for the "by adam" text
by_adam_crop = pygame.transform.scale(by_adam_crop, (WIDTH, HEIGHT))

name_crop = pygame.image.load(rf'PNG\name_crop.png')  # when the input name is being drawn
name_crop = pygame.transform.scale(name_crop, (WIDTH, HEIGHT))

wait_key_crop = pygame.image.load(rf'PNG\wait_key_crop.png')
wait_key_crop = pygame.transform.scale(wait_key_crop, (WIDTH, HEIGHT))

cards_crop = pygame.image.load(rf'PNG\cards_crop.png')
cards_crop = pygame.transform.scale(cards_crop, (WIDTH, HEIGHT))

cards_logo = pygame.image.load('PNG\cards_bg.png')  # the logo of the cards from the beginning
cards_logo = pygame.transform.scale(cards_logo, (int(WIDTH/2.5), int(HEIGHT/1.4234)))

cards_logo_crop = pygame.image.load(rf'PNG\bg_crop.png')  # the INTRO_BACKG cropped for the card logo
cards_logo_crop = pygame.transform.scale(cards_logo_crop, (WIDTH, HEIGHT))

line_above_cards = pygame.image.load(rf'PNG\pas.png')  # the line for the choosing arrow. part of the second background
line_above_cards = pygame.transform.scale(line_above_cards, (WIDTH, HEIGHT))

pick_filter = pygame.image.load(r'PNG\pick_filter.png')
pick_filter = pygame.transform.scale(pick_filter, (WIDTH, HEIGHT))

used_cards_filter = pygame.image.load(r'PNG\used_cards_filter1.png')
used_cards_filter = pygame.transform.scale(used_cards_filter, (WIDTH, HEIGHT))

red_arrow = pygame.image.load(r'PNG\red_arrow.png')
red_arrow = pygame.transform.scale(red_arrow, (int(HEIGHT/40), int(HEIGHT/40)))

drop1 = pygame.image.load(rf'PNG\drop1BUTT.png')
drop2 = pygame.image.load(rf'PNG\drop2BUTT.png')
drop_crop = pygame.image.load(fr'PNG\drop_crop.png')
drop_crop = pygame.transform.scale(drop_crop, (WIDTH, HEIGHT))

yaniv1 = pygame.image.load(rf'PNG\yaniv1BUTT.png')
yaniv2 = pygame.image.load(rf'PNG\yaniv2BUTT.png')
yaniv_b_crop = pygame.image.load(fr'PNG\yaniv_B_crop.png')
yaniv_b_crop = pygame.transform.scale(yaniv_b_crop, (WIDTH, HEIGHT))

scale = (int(WIDTH/15), int(WIDTH/15))
drop1 = pygame.transform.scale(drop1, scale)
drop2 = pygame.transform.scale(drop2, scale)
yaniv1 = pygame.transform.scale(yaniv1, scale)
yaniv2 = pygame.transform.scale(yaniv2, scale)

#-------------------------------------------------------------


wait_for_key = myfont_small.render('PRESS ANY KEY TO CONTINUE', True, WHITE)
wait_for_key_rect = wait_for_key.get_rect()
wait_for_key_rect.center = (WIDTH/2, HEIGHT/1.1)

FPS = 60

def draw_window(image1):
    im = pygame.transform.scale(image1, (WIDTH, HEIGHT))
    WIN.blit(im, (0, 0))
    pygame.display.update()

# List_updates = []

soundObj = pygame.mixer.Sound(r'Music\ElevatorMusic.wav')
ww_music = pygame.mixer.Sound(r'Music\WildWestern.wav')

def draw_opensc():
    true = True
    while true:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                true = False
    ww_music.play()
    WIN.blit(intro_backg, (0, 0))
    pygame.display.flip()
    time.sleep(0.5)
    wlc = myfont_small.render('Welcome to:', True, WHITE)
    #WIN.blit(wlc, (WIDTH/12, HEIGHT/4))
    fade_in(wlc, (WIDTH/12, HEIGHT/4), 2, [[intro_backg, (0, 0)]])

    time.sleep(0.6)
    objects = [[intro_backg, (0, 0)], [wlc, (WIDTH/12, HEIGHT/4)]]
    text = myfont_BIG.render('Yaniv', True, WHITE)
    #textRect = text.get_rect()
    #textRect.center = (WIDTH/4, HEIGHT/3.5)
    pos = (int(WIDTH/13), HEIGHT/3.3)
    fade_in(text, pos, 4, [[yaniv_crop, (0, 0)]])
    objects.append([text, pos])
    #WIN.blit(text, (int(WIDTH/13), HEIGHT/3.3))


    #print(f'intro_backgW {bg.get_width()} and intro_backgH {bg.get_height()}')

    fade_in(cards_logo, (WIDTH/2, HEIGHT/7), 8, [[cards_logo_crop, (0, 0)]])
    #WIN.blit(bg, (WIDTH/2, HEIGHT/7))
    #time.sleep(2)
    #pygame.display.update()
    by = myfont_medium.render('By: Adam Kol', True, WHITE)
    x = -WIDTH/5
    power = WIDTH/12.8
    WIN.blit(by, (x, HEIGHT/1.6))
    pygame.display.update()
    #cl3 = pygame.time.Clock()
    while x < WIDTH/3.5:
        #cl3.tick(25)
        x += power/2
        power = power/1.25 + 10

        WIN.blit(by_adam_crop, (0, 0))
        WIN.blit(by, (x, HEIGHT/1.6))

        pygame.display.update()

    time.sleep(1.4)
    #WIN.blit(any, textRect)
    #pygame.display.update()

    alpha = 0
    down = True
    #cl2 = pygame.time.Clock()
    while True:
        #cl2.tick(20)
        WIN.blit(wait_key_crop, (0, 0))
        if alpha > 4 and down:
            alpha -= 5

        elif alpha == 0:
            down = False
            alpha += 5

        elif alpha < 251 and not down:
            alpha += 5

        elif alpha == 255:
            down = True
            alpha -= 5

        wait_for_key.set_alpha(alpha)
        WIN.blit(wait_for_key, wait_for_key_rect)
        pygame.display.update()
        #
        # #time.sleep(0.7)
        #
        # WIN.blit(any, textRect)
        # pygame.display.update()

        #time.sleep(0.7)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

def fade_out(object, pos, secs, other_objects):
    alpha = 255
    times = 0
    cl = pygame.time.Clock()
    while alpha > 0:
        #print(alpha)
        for objects in other_objects:
            WIN.blit(objects[0], objects[1])
        cl.tick(20)
        time.sleep(0.04)
        times += 0.06
        object.set_alpha(alpha)
        WIN.blit(object, pos)
        pygame.display.update()
        alpha -= 8
        if times > secs:
            object.set_alpha(0)
            for objects in other_objects:
                WIN.blit(objects[0], objects[1])
            WIN.blit(object, pos)
            pygame.display.update()
            #print("end fade")
            return
    object.set_alpha(0)
    for objects in other_objects:
        WIN.blit(objects[0], objects[1])
    WIN.blit(object, pos)
    pygame.display.update()

def fade_in(object, pos, secs, other_objects):
    alpha = 0
    times = 0
    cl = pygame.time.Clock()
    while alpha < 256:
        #print(alpha)
        for objects in other_objects:
            WIN.blit(objects[0], objects[1])
        cl.tick(20)
        time.sleep(0.04)
        times += 0.06
        object.set_alpha(alpha)
        WIN.blit(object, pos)
        pygame.display.update()
        alpha += 8
        if times > secs:
            object.set_alpha(255)
            WIN.blit(object, pos)
            pygame.display.update()
            #print("end fade")
            return


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    # rot_rect = orig_rect.copy()
    # rot_rect.center = rot_image.get_rect().center
    # rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def draw_enemy_cards(sums):
    '''the function gets a list of
    the cards amount of each player
    means the len is the players number'''
    card_h = WIDTH/6
    card_w = card_h*1.3

    if len(sums) == 1:
        how_many = sums[0]

        if how_many > 7:
            e_cards = pygame.image.load(rf'PNG\red_back_7+o.png')
        else:
            e_cards = pygame.image.load(rf'PNG\red_back_{how_many}.png')

        e_cards = pygame.transform.scale(e_cards, (int(card_w), int(card_h)))
        e_cards = pygame.transform.rotate(e_cards, 180)


        im_rect = e_cards.get_rect()
        im_rect.center = (WIDTH/2, HEIGHT/10)

        WIN.blit(e_cards, im_rect)
        pygame.display.flip()

    card_h = WIDTH/7.2
    card_w = card_h*1.3

    x, y = WIDTH - 130, 130
    if len(sums) == 2:
        angle = 135
        #x = WIDTH/10
        for num in sums:
            if num > 7:
                e_cards = pygame.image.load(rf'PNG\red_back_7+o.png')
            else:
                e_cards = pygame.image.load(rf'PNG\red_back_{num}.png')

            e_cards = pygame.transform.scale(e_cards, (int(card_w), int(card_h)))
            e_cards = pygame.transform.rotate(e_cards, angle)

            im_rect = e_cards.get_rect()
            im_rect.center = (x, y)

            WIN.blit(e_cards, im_rect)
            pygame.display.flip()
            angle += 90
            x = 130

    x, y = WIDTH - 90, HEIGHT/2
    if len(sums) == 3:
        angle = 90
        #x, y = 100, 100
        i = 0
        for num in sums:
            if num > 7:
                e_cards = pygame.image.load(rf'PNG\red_back_7+o.png')
            else:
                e_cards = pygame.image.load(rf'PNG\red_back_{num}.png')

            e_cards = pygame.transform.scale(e_cards, (int(card_w), int(card_h)))
            e_cards = pygame.transform.rotate(e_cards, angle)

            im_rect = e_cards.get_rect()
            im_rect.center = (x, y)

            WIN.blit(e_cards, im_rect)
            pygame.display.flip()
            angle += 90
            x -= WIDTH/2 - 90
            y = HEIGHT/2
            if i == 0:
                y = 90
            i += 1

    card_h = WIDTH/7.8
    card_w = card_h*1.3

    if len(sums) == 4:
        angle = 90
        #x, y = 100, 100
        i = 0
        for num in sums:
            if num > 7:
                e_cards = pygame.image.load(rf'PNG\red_back_7+o.png')
            else:
                e_cards = pygame.image.load(rf'PNG\red_back_{num}.png')

            e_cards = pygame.transform.scale(e_cards, (int(card_w), int(card_h)))
            e_cards = pygame.transform.rotate(e_cards, angle)

            im_rect = e_cards.get_rect()
            im_rect.center = (x, y)

            WIN.blit(e_cards, im_rect)
            pygame.display.flip()
            angle = 270
            x -= (WIDTH - 180)/3
            y = HEIGHT/2
            if i == 0 or i == 1:
                angle = 180
                y = 90
            i += 1


def draw_card_test():
    crd = pygame.image.load(r'PNG\red_back.png')

    card_w = 691/5
    card_h = 1056/5

    back_card = pygame.transform.scale(crd, (int(card_w), int(card_h)))
    rect = back_card.get_rect()
    rect.center = (card_w, card_h)

    WIN.blit(back_card, rect)
    pygame.display.flip()

def draw_wating_for_players():

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
        WIN.blit(intro_backg, (0, 0))
        # textRect.center = (WIDTH/2, y)
        WIN.blit(text, (int(WIDTH/2.5), y))
        pygame.display.update()

        y -= 1

    y += 1
    loop = True
    while loop:
        WIN.blit(intro_backg, (0, 0))
        pygame.display.update()


        WIN.blit(text, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(intro_backg, (0, 0))
        WIN.blit(text_1dot, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(intro_backg, (0, 0))
        WIN.blit(text_2dot, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)
        WIN.blit(intro_backg, (0, 0))
        WIN.blit(text_3dot, (int(WIDTH/2.5), y))
        pygame.display.update()
        time.sleep(0.3)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                soundObj.stop()
                loop = False
def draw_cards(cards, greened, redded, whited, dot_index, new_num=False, pick=False):

    if new_num:
        WIN.blit(cards_crop, (0, 0))
    cards_num = len(cards)
    ratio = 6
    dif = WIDTH/10.5
    # if cards_num > 5:
    #     dif = WIDTH/18
    i = WIDTH/2 - 0.5*(cards_num - 1)*dif
    y = HEIGHT - HEIGHT/7

    if pick:
        #print("drawing pick")
        ratio = 7
        y = HEIGHT/2 - HEIGHT/35
        dif = WIDTH/11
        i = WIDTH/3 - 0.5*(cards_num - 1)*dif

    card_w = 691/ratio
    card_h = 1056/ratio
    for item in cards:

        card = fr'PNG\{item}.png'
        card_image = pygame.image.load(card)

        card_image = pygame.transform.scale(card_image, (int(card_w), int(card_h)))

        #print(f'imageW {image.get_width()} and imageH {image.get_height()}')

        card_rect = card_image.get_rect()
        card_rect.center = (i, y)

        WIN.blit(card_image, card_rect)

        if cards.index(item) in dot_index:
            #print("drawing red idot")
            WIN.blit(red_arrow, (i + card_w/4, y - card_h/2.3))

        if not -1 in whited:
            if not cards.index(item) in whited:
                white_filter = pygame.image.load(rf'PNG\white_filter.png')
                white_filter = pygame.transform.scale(white_filter, (int(card_w), int(card_h)))
                WIN.blit(white_filter, card_rect)

        if cards.index(item) in greened:
            green_filter = pygame.image.load(rf'PNG\green_filter.png')
            green_filter = pygame.transform.scale(green_filter, (int(card_w), int(card_h)))
            WIN.blit(green_filter, card_rect)

        if cards.index(item) in redded:
            red_filter = pygame.image.load(rf'PNG\red_filter.png')
            red_filter = pygame.transform.scale(red_filter, (int(card_w), int(card_h)))
            WIN.blit(red_filter, card_rect)

        pygame.display.flip()

        i += dif

    return
    # if index_of_green == None:
    #     return False
    #
    # x = i + dif*index_of_green
    #
    # green_filter = pygame.image.load(rf'PNG\green_filter.png')
    # green_filter = pygame.transform.scale(green_filter, (int(card_w), int(card_h)))
    #
    # filter_rect = green_filter.get_rect()
    # filter_rect.center = (x, HEIGHT - HEIGHT/7)
    #
    # WIN.blit(green_filter, filter_rect)
    # pygame.display.flip()
    #
    # return True

def draw_arrow_choose(cards, index):

    #cropped_region = pygame.Rect(int(WIDTH/9), int(HEIGHT - HEIGHT/3), int(WIDTH/1.3), int(HEIGHT/25))
    #cropped_subsurf = pygame.source_surf.subsurface(cropped_region)
    WIN.blit(line_above_cards, (0, 0))
    pygame.display.update()

    cards_num = len(cards)

    vi_dot = pygame.image.load(rf'PNG\arrow_white.png')
    dot_image = pygame.transform.scale(vi_dot, (int(WIDTH/70), int(WIDTH/70)))

    dif = WIDTH/10.5

    if cards_num > 5:
        dif = WIDTH/18
    i = WIDTH/2 - 0.5*(cards_num - 1)*dif

    x = i + dif*index
    dot_rect = dot_image.get_rect()
    dot_rect.center = (x, HEIGHT - HEIGHT/3.4)


    WIN.blit(dot_image, dot_rect)
    #pygame.display.flip()


    # cards_num = len(cards)
    # ratio = 6
    # dif = WIDTH/10.5
    # if cards_num > 4:
    #     dif = WIDTH/18
    # i = WIDTH/2 - 0.5*(cards_num - 1)*dif
    # card_w = 691/ratio
    # card_h = 1056/ratio
    #
    # print(type(bigger))
    # big = cards[bigger]
    # print(type(big))
    # card = fr'PNG\{big}.png'
    # card_image = pygame.image.load(card)
    #
    # card_image = pygame.transform.scale(card_image, (int(card_w*1.1), int(card_h*1.1)))
    # card_rect = card_image.get_rect()
    # card_rect.center = (i, HEIGHT - HEIGHT/7)

    # for item in cards:
    #     if item != cards[bigger]:
    #         card = fr'PNG\{item}.png'
    #         card_image = pygame.image.load(card)
    #
    #         card_image = pygame.transform.scale(card_image, (int(card_w), int(card_h)))
    #         card_rect = card_image.get_rect()
    #         card_rect.center = (i, HEIGHT - HEIGHT/7)
    #         #bigger.remove(item)
    #         #print(f'imageW {image.get_width()} and imageH {image.get_height()}')
    #
    #         WIN.blit(card_image, card_rect)
    #         pygame.display.flip()
    #         i += dif
    # return

def draw_stack(stack, bigger=False, crop=True):
    stack_crop = pygame.image.load(rf'PNG\stack_crop.png')
    stack_crop = pygame.transform.scale(stack_crop, (WIDTH, HEIGHT))
    if crop:
        WIN.blit(stack_crop, (0, 0))
    if stack <= 5:
        stack_back = pygame.image.load(rf'PNG\stack_{stack}.png')

        card_h = WIDTH/5
        if bigger:
            card_h = WIDTH/4.5

        card_w = card_h*1.3
        stack_back = pygame.transform.scale(stack_back, (int(card_w), int(card_h)))

        im_rect = stack_back.get_rect()
        im_rect.center = (WIDTH - WIDTH/3, HEIGHT/2 - HEIGHT/35)

        WIN.blit(stack_back, im_rect)
        pygame.display.flip()
    else:  # stack is bigger than 5
        stack_back = pygame.image.load(rf'PNG\stack_5.png')

        card_h = WIDTH/5
        card_w = card_h*1.3

        stack_back = pygame.transform.scale(stack_back, (int(card_w), int(card_h)))

        im_rect = stack_back.get_rect()
        im_rect.center = (WIDTH - WIDTH/3, HEIGHT/2 - HEIGHT/35)

        WIN.blit(stack_back, im_rect)
        pygame.display.flip()

def choosable(cards_num, size):
    dif = WIDTH/9
    if cards_num > 4:
        dif = WIDTH/18

    oh = pygame.mouse.get_pressed(3)
    print(oh)

def add_green(cards, index, bools):
    '''the dunction gets the cards array and the
    index of the cards that is chosen. no return,
    draws the green filter'''
    cards_num = len(cards)

    card_w = 691/6
    card_h = 1056/6

    dif = WIDTH/10.5
    if cards_num > 4:
        dif = WIDTH/18
    i = WIDTH/2 - 0.5*(cards_num - 1)*dif
    x = i + dif*index

    green_filter = pygame.image.load(rf'PNG\green_filter.png')
    if bools == False:
        green_filter = pygame.image.load(rf'PNG\{cards[index]}.png')

    green_filter = pygame.transform.scale(green_filter, (int(card_w), int(card_h)))

    filter_rect = green_filter.get_rect()
    filter_rect.center = (x, HEIGHT - HEIGHT/7)

    WIN.blit(green_filter, filter_rect)
    pygame.display.flip()

def draw_button(image, image_pressed, crop, pos, on_it=False):

    #drop_crop = pygame.image.load(fr'PNG\drop_crop.png')
    #drop_crop = pygame.transform.scale(drop_crop, (WIDTH, HEIGHT))
    WIN.blit(crop, (0, 0))

    '''the function draws the "drop" button'''
    the_rect = image.get_rect()
    the_rect.center = pos

    the_rect2 = image_pressed.get_rect()
    the_rect2.center = pos

    if not on_it:
        WIN.blit(image, the_rect)
        pygame.display.flip()
        return
    WIN.blit(image_pressed, the_rect2)
    pygame.display.flip()
    return

def used_cards(chosen_cards, filter=True):
    '''the function gets the cards chosen and the cards in general
    by the player and draws them in the used cards'''
    if filter:
        WIN.blit(used_cards_filter, (0, 0))
    cards_num = len(chosen_cards)
    if cards_num == 1:
        card = pygame.image.load(fr'PNG\{chosen_cards[0]}.png')
        card_w = 691/5
        card_h = 1056/5

        card_image = pygame.transform.scale(card, (int(card_w), int(card_h)))

        angle = random.randint(-15, 15)
        card_image = pygame.transform.rotate(card_image, angle)
        card_rect = card_image.get_rect()
        card_rect.center = (WIDTH/3, HEIGHT/2 - HEIGHT/35)

        WIN.blit(card_image, card_rect)

    elif cards_num == 2:
        card1 = pygame.image.load(fr'PNG\{chosen_cards[0]}.png')
        card2 = pygame.image.load(fr'PNG\{chosen_cards[1]}.png')

        card_w = 691/6
        card_h = 1056/6

        card1_image = pygame.transform.scale(card1, (int(card_w), int(card_h)))
        card2_image = pygame.transform.scale(card2, (int(card_w), int(card_h)))

        angle1 = random.randint(-15, 15)
        angle2 = random.randint(-15, 15)

        card1_image = pygame.transform.rotate(card1_image, angle1)
        card1_rect = card1_image.get_rect()
        card1_rect.center = (WIDTH/3 - card_w/3, HEIGHT/2 - HEIGHT/35)

        card2_image = pygame.transform.rotate(card2_image, angle2)
        card2_rect = card2_image.get_rect()
        card2_rect.center = (WIDTH/3 + card_w/3, HEIGHT/2 - HEIGHT/35)

        WIN.blit(card1_image, card1_rect)
        WIN.blit(card2_image, card2_rect)

    elif cards_num > 2:
        card_w = 691/(cards_num + 1.5)
        card_h = 1056/(cards_num + 1.5)

        dif = card_w/2
        place = WIDTH/3 - ((cards_num - 1)/2)*dif
        for item in chosen_cards:
            card = pygame.image.load(fr'PNG\{item}.png')
            angle = random.randint(-5, 5)

            card = pygame.transform.scale(card, (int(card_w), int(card_h)))

            card = pygame.transform.rotate(card, angle)
            card_rect = card.get_rect()
            card_rect.center = (place, HEIGHT/2 - HEIGHT/35)

            WIN.blit(card, card_rect)
            place += dif


    pygame.display.flip()
    # card = pygame.image.load(fr'PNG\{chosen_cards}.png')
    #
    # card_w = 691/6
    # card_h = 1056/6
    #
    # card_image = pygame.transform.scale(card, (int(card_w), int(card_h)))
    #
    # angle = random.randint(-15, 15)
    # card_image = pygame.transform.rotate(card_image, angle)
    # card_rect = card_image.get_rect()
    # card_rect.center = (WIDTH/3, HEIGHT/2 - HEIGHT/35)
    #
    # WIN.blit(card_image, card_rect)
def get_name():
    '''the function takes the name of the player and draws the name'''
    #print("ohhhhhh")

    WIN.blit(intro_backg, (0, 0))
    pygame.display.flip()

    name_enter = myfont_medium_plus.render('enter your name', True, WHITE)

    fade_in(name_enter, (40, 40), 2, [[intro_backg, (0, 0)]])
    pygame.display.flip()

    player_name = ''
    name_finished = False
    while not name_finished:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    print("backspace")
                    player_name = player_name[:-1]
                elif len(player_name) < 30:  # length of the name up to 30
                    print(event.unicode)
                    player_name += event.unicode
                if event.key == pygame.K_RETURN:
                    print("enter")
                    name_finished = True

        name = myfont_medium_plus.render(f'{player_name}', True, WHITE)
        name_rect = name.get_rect()
        name_rect.center = (WIDTH/2, HEIGHT/2)
        WIN.blit(name_crop, (0, 0))
        WIN.blit(name, (name_rect))

        pygame.display.flip()

    ww_music.stop()
    return player_name

def choose(cards, last_cards):
    '''the function is responsible to return valid cards to continue playing
    returns a list for [bool=True if its a regular turn, False if Yaniv
                        ]'''

    cards_greened = []
    chosen_cards = []
    order = []
    index = 0

    is_stack_big = False

    finished_choose = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            mx, my = pygame.mouse.get_pos()
            if not finished_choose:
                if event.type == pygame.KEYUP:
                    print("Here")
                    #draw_arrow_choose(cards, index)
                    if event.key == pygame.K_LEFT:
                        if index == 0:
                            index = 0
                            draw_arrow_choose(cards, index)
                        else:
                            index -= 1
                            draw_arrow_choose(cards, index)
                    if event.key == pygame.K_RIGHT:
                        if index == len(cards) - 1:
                            index = len(cards) - 1
                            draw_arrow_choose(cards, index)
                        else:
                            index += 1
                            draw_arrow_choose(cards, index)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            if index not in cards_greened:
                                cards_greened.append(index)
                                chosen_cards.append(cards[index])
                                draw_cards(cards, cards_greened, [], [-1], [])
                            else:
                                cards_greened.remove(index)
                                chosen_cards.remove(cards[index])
                                draw_cards(cards, cards_greened, [], [-1], [])
                pygame.display.flip()
            #mx, my = pygame.mouse.get_pos()
                if mx > 985 and mx < 1065 and my > 593 and my < 642:
                    draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7), True)
                    #for event in pygame.event.get():
                    #pygame.event.get()
                    if pygame.mouse.get_pressed()[0]:
                        is_valid, order = cm.check_valid(chosen_cards)
                        print("chosen cards:", chosen_cards, "is valid is", is_valid, "order is;", order)
                        if len(chosen_cards) == 0:
                            is_valid = False
                        if is_valid:
                            #print("valid. cards: ", cards, "chosen cards:", chosen_cards)
                            for card in chosen_cards:
                                cards.remove(card)
                            draw_cards(cards, [], [], [-1], [], True)
                            index = 0
                            draw_arrow_choose(order, index)
                            draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7), False)
                            finished_choose = True
                            # return [True, chosen_cards, cards]
                        if not is_valid:  # else means the chosen cards invalid
                            print("invalid", cards_greened)
                            draw_cards(cards, [], cards_greened, [-1], [])
                            time.sleep(1)
                            draw_cards(cards, [], [], [-1], [])
                            chosen_cards.clear()
                            cards_greened.clear()
                            index = 0
                            draw_arrow_choose(cards, index)
                else:
                    draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7))

                if mx > 217 and mx < 296 and my > 594 and my < 642:
                        draw_button(yaniv1, yaniv2, yaniv_b_crop, (WIDTH/5, HEIGHT - HEIGHT/7), True)
                        #for event in pygame.event.get():
                        if pygame.mouse.get_pressed()[0]:
                            is_valid, order = cm.sum_cards(cards) <= 7
                            if is_valid:
                                return [YANIV_MESSAGE]
                            else:  # else means the chosen cards invalid
                                cards_greened.clear()
                                for i in range(0, len(cards)):
                                    cards_greened.append(i)
                                draw_cards(cards, [], cards_greened, [-1], [])
                                time.sleep(1)
                                draw_cards(cards, [], [], [-1], [])
                                index = 0
                                draw_arrow_choose(cards, index)
                                chosen_cards.clear()
                                cards_greened.clear()
                else:
                    draw_button(yaniv1, yaniv2, yaniv_b_crop, (WIDTH/5, HEIGHT - HEIGHT/7))
            else:
                WIN.blit(yaniv_b_crop, (0, 0))
                WIN.blit(drop_crop, (0, 0))
                pygame.display.flip()
                ans = ask_deck_or_last(last_cards)
                if ans == -1:
                    print('deck returned')
                    return ['DECK', order, cards]
                else:
                    print("last returned")
                    cards.append(ans)
                    draw_cards(cards, [], [], [-1], [])
                    return ['LAST', order, cards]
        # STACK
        #mx, my = pygame.mouse.get_pos()
            #print(f'x: {mx}, y: {my}')


            pygame.display.flip()

        # if mx > 985 and mx < 1065 and my > 593 and my < 642:
        #         draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7), True)
        #         #for event in pygame.event.get():
        #         #pygame.event.get()
        #         if pygame.mouse.get_pressed()[0] and not finished_choose:
        #             is_valid = cm.check_valid(chosen_cards)
        #             print("chosen cards:", chosen_cards, "is valid is", is_valid)
        #             if len(chosen_cards) == 0:
        #                 is_valid = False
        #             if is_valid:
        #                 #print("valid. cards: ", cards, "chosen cards:", chosen_cards)
        #                 for card in chosen_cards:
        #                     cards.remove(card)
        #                 draw_cards(cards, [], [], True)
        #                 index = 0
        #                 draw_arrow_choose(cards, index)
        #                 draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7), False)
        #                 finished_choose = True
        #                 # return [True, chosen_cards, cards]
        #             if not is_valid:  # else means the chosen cards invalid
        #                 print("invalid", cards_greened)
        #                 draw_cards(cards, [], cards_greened)
        #                 time.sleep(1)
        #                 draw_cards(cards, [], [])
        #                 chosen_cards.clear()
        #                 cards_greened.clear()
        #                 index = 0
        #                 draw_arrow_choose(cards, index)
        #         else:
        #             draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7))
        # else:
        #     draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7))
        #
        # if mx > 217 and mx < 296 and my > 594 and my < 642:
        #         draw_button(yaniv1, yaniv2, yaniv_b_crop, (WIDTH/5, HEIGHT - HEIGHT/7), True)
        #         #for event in pygame.event.get():
        #         if pygame.mouse.get_pressed()[0] and not finished_choose:
        #             is_valid = cm.sum_cards(cards) <= 7
        #             if is_valid:
        #                 return [False, YANIV_MESSAGE]
        #             else:  # else means the chosen cards invalid
        #                 cards_greened.clear()
        #                 for i in range(0, len(cards)):
        #                     cards_greened.append(i)
        #                 draw_cards(cards, [], cards_greened)
        #                 time.sleep(1)
        #                 draw_cards(cards, [], [])
        #                 index = 0
        #                 draw_arrow_choose(cards, index)
        #                 chosen_cards.clear()
        #                 cards_greened.clear()
        #         else:
        #             draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7))
        # else:
        #     draw_button(yaniv1, yaniv2, yaniv_b_crop, (WIDTH/5, HEIGHT - HEIGHT/7))
def ask_deck_or_last(last_cards):

    stack_filter = pygame.image.load(r'PNG\stack_5_white_filter.png')
    stack_filter = pygame.transform.scale(stack_filter, (int(WIDTH/5*1.3), int(WIDTH/5)))
    s_rect = stack_filter.get_rect()
    s_rect.center = (WIDTH - WIDTH/3, HEIGHT/2 - HEIGHT/35)

    if len(last_cards) > 1:
        last_cards = [last_cards[0], last_cards[-1]]
    WIN.blit(pick_filter, (0, 0))
    draw_cards(last_cards, [], [], [-1], [], False, True)
    draw_stack(5, False, False)
    choose_txt = myfont_small.render('pick with the arrow keys', True, WHITE)
    choose_txt_rect = choose_txt.get_rect()
    choose_txt_rect.center = (WIDTH/2, HEIGHT/3.5)
    WIN.blit(choose_txt, choose_txt_rect)
    pygame.display.flip()

    index = 0
    choose = False

    draw_cards(last_cards, [], [], [index], [], False, True)
    WIN.blit(stack_filter, s_rect)
    while not choose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if index == 0:
                        index = len(last_cards)
                        #WIN.blit(red_arrow, (WIDTH - WIDTH/3.1, HEIGHT/2 - HEIGHT/6.2))
                        draw_stack(5, False, False)
                        draw_cards(last_cards, [], [], [index], [], False, True)
                    elif index == len(last_cards):
                        draw_stack(5, False, False)
                        WIN.blit(stack_filter, s_rect)
                        index = len(last_cards) - 1
                        draw_cards(last_cards, [], [], [index], [], False, True)
                    else:
                        index = 0
                        draw_cards(last_cards, [], [], [index], [], False, True)
                if event.key == pygame.K_RIGHT:
                    if index == 0 and len(last_cards) == 1:
                        index = len(last_cards)
                        #WIN.blit(red_arrow, (WIDTH - WIDTH/3.1, HEIGHT/2 - HEIGHT/6.2))
                        draw_stack(5, False, False)
                        draw_cards(last_cards, [], [], [index], [], False, True)
                    elif index == 0:
                        index += len(last_cards) - 1
                        draw_cards(last_cards, [], [], [index], [], False, True)
                    elif index == len(last_cards) - 1:
                        index = len(last_cards)
                        #WIN.blit(red_arrow, (WIDTH - WIDTH/3.1, HEIGHT/2 - HEIGHT/6.2))
                        #WIN.blit(stack_filter, s_rect)
                        draw_stack(5, False, False)
                        draw_cards(last_cards, [], [], [index], [], False, True)
                    elif index == len(last_cards):
                        #draw_stack(5, False, False)
                        WIN.blit(stack_filter, s_rect)
                        index = 0
                        draw_cards(last_cards, [], [], [index], [], False, True)
                if event.key == pygame.K_RETURN:
                    if index == len(last_cards):  # means its deck
                        return - 1
                    return last_cards[index]
        pygame.display.flip()

    #question = choose_txt = myfont_medium.render('draw pile:', True, WHITE)

def draw_back_to_game(cards, all_sums, stack, last_cards):
    WIN.blit(blue_backg, (0, 0))
    draw_cards(cards, [], [], [-1], [])
    draw_enemy_cards(all_sums)
    draw_stack(stack)
    if len(last_cards) == 0:
        used_cards(last_cards, False)
    else:
        used_cards(last_cards)
    pygame.display.flip()


def main():
    #draw_opensc()
    #name = get_name()
    run = True
    #draw_wating_for_players()
    WIN.blit(intro_backg, (0, 0))
    pygame.display.update()
    #bigger = []
    index = 0
    sums = [5, 5, 5]

    #draw_enemy_cards(sums)
    draw_window(blue_backg)
    draw_stack(5)
    draw_enemy_cards(sums)
    cards = [10, 23, 53, 50, 22]
    cards_greened = []
    draw_arrow_choose(cards, 0)
    draw_cards(cards, cards_greened, [], [-1], [])

    draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7))
    draw_button(yaniv1, yaniv2, yaniv_b_crop, (WIDTH/5, HEIGHT - HEIGHT/7))

    last_cards = [1]
    is_valid, order = cm.check_valid(last_cards)
    used_cards(order, False)
    res = choose(cards, order)
    last_cards.remove(res[-1][-1])
    draw_back_to_game(res[-1], sums, 5, last_cards)
    if len(last_cards) == 0:
        used_cards(res[1], False)
    else:
        used_cards(res[1])
    #if res[0]:
        #deck_or_last = pick_dl()  # pick deck or last
        #used_cards(res[1])
        #print(res[2])
    #else:
        #print("YANIV!")
    is_stack_big = False
    #is_on_drop = False
    print("draw finished")
    while run:
        #clock.tick(FPS)
        index = 0

        #pick_dl()

        #pick_dl()
        # mx, my = pygame.mouse.get_pos()
        # if mx > 790 and mx < 920 and my > 245 and my < 440:
        #     if not is_stack_big:
        #         draw_stack(5, bigger=True)
        #         is_stack_big = True
        #         if pygame.mouse.get_pressed()[0]:
        #             print("DECK CHOSE")
        # else:
        #     if is_stack_big:
        #         draw_stack(5)
        #         is_stack_big = False
        #index_of_green = -1
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #
        #     if event.type == pygame.KEYUP:
        #         print("Here")
        #     #draw_arrow_choose(cards, index)
        #         if event.key == pygame.K_LEFT:
        #             if index == 0:
        #                 index = 0
        #                 draw_arrow_choose(cards, index)
        #             else:
        #                 index -= 1
        #                 draw_arrow_choose(cards, index)
        #         if event.key == pygame.K_RIGHT:
        #             if index == len(cards) - 1:
        #                 index = len(cards) - 1
        #                 draw_arrow_choose(cards, index)
        #             else:
        #                 index += 1
        #                 draw_arrow_choose(cards, index)
        #
        #         if event.type == pygame.KEYUP:
        #             if event.key == pygame.K_SPACE:
        #                 if index not in cards_greened:
        #                     cards_greened.append(index)
        #                     draw_cards(cards, cards_greened)
        #                 else:
        #                     cards_greened.remove(index)
        #                     draw_cards(cards, cards_greened)
        #                     #cards_greened.remove(index)
        #
        # pygame.display.flip()
        #
        #
        #
        #
        # # keys = pygame.key.release()
        # # if keys[pygame.K_LEFT]:
        # #     WIN.blit(line_above_cards, (0, 0))
        # #     #draw_arrow_choose(cards, index)
        # #     if index == 0:
        # #         index = 0
        # #         draw_arrow_choose(cards, index)
        # #     else:
        # #         index -= 1
        # #         draw_arrow_choose(cards, index)
        # # if keys[pygame.K_RIGHT]:
        # #     WIN.blit(line_above_cards, (0, 0))
        # #     if index == len(cards) - 1:
        # #         index = len(cards) - 1
        # #         draw_arrow_choose(cards, index)
        # #     else:
        # #         index += 1
        # #         draw_arrow_choose(cards, index)
        #
        #
        # #print(index)
        # #print("Hello")
        # sums = [2, 6, 23, 8]
        # #print("draw finished")
        #
        # #print("drawing")
        # #draw_enemy_cards(sums)
        # mx, my = pygame.mouse.get_pos()
        # if mx > 790 and mx < 920 and my > 245 and my < 440:
        #         if not is_stack_big:
        #             draw_stack(5, bigger=True)
        #             is_stack_big = True
        # else:
        #     if is_stack_big:
        #         draw_stack(5)
        #         is_stack_big = False
        # #draw_cards(cards)
        # pygame.display.flip()
        #
        # if mx > 985 and mx < 1065 and my > 593 and my < 642:
        #         draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7), True)
        #         for event in pygame.event.get():
        #             if event.type == pygame.MOUSEBUTTONDOWN:
        #                 used_cards([2, 15])
        # else:
        #     draw_button(drop1, drop2, drop_crop, (WIDTH - WIDTH/5, HEIGHT - HEIGHT/7))
        #
        #
        #         # if not is_on_drop:
        #         #     is_on_drop = True
        #         #     drop_button(is_on_drop)
        # # if not (mx > 985 and mx < 1065):
        # #     if not (my > 593 and my < 642):
        # #         drop_button()
        # pygame.display.flip()
        #     # if is_on_drop:
        #     #     is_on_drop = False
        #     #     drop_button(is_on_drop)
        #
        # #match()
        # mx, my = pygame.mouse.get_pos()
        # #size = draw_cards(cards, mx, my)
        #
        # #choosable(len(cards), size)
        # #mx, my = pygame.mouse.get_pos()
        # print(f'x: {mx}, y: {my}')


    pygame.quit()


if __name__ == '__main__':
    main()
