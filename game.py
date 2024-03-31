import pygame
from random import *
from time import *

clock = pygame.time.Clock()
pygame.init()

# Анимация
walk_left = [
    pygame.image.load('images/player_left.png'),
    pygame.image.load('images/player_left2.png')
]
walk_right = [
    pygame.image.load('images/player_right.png'),
    pygame.image.load('images/player_right2.png')
]

# Константы
screen_x, screen_y = 480, 740
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("CleanCom")
pygame.display.set_icon(pygame.image.load('images/icon.png'))
bg = pygame.image.load('images/1.jpg')
foot = pygame.image.load('images/foot.png')
dirty = pygame.image.load('images/dirty.png')
dirty1 = pygame.image.load('images/dirty1.png')
fontWIN = pygame.font.Font('fonts/Roboto-black.ttf', 80)
fontDEF = pygame.font.Font('fonts/Roboto-black.ttf', 40)
fontTIME = pygame.font.Font('fonts/Roboto-black.ttf', 50)
fontCOUNT = pygame.font.Font('fonts/Roboto-black.ttf', 50)
fontCC = pygame.font.Font('fonts/Roboto-black.ttf', 80)
fontTip = pygame.font.Font('fonts/Roboto-black.ttf', 25)
fontP = pygame.font.Font('fonts/Roboto-black.ttf', 25)

textWIN = fontWIN.render('Премия!', True, (255,0,0))
textDEF = fontDEF.render('Начните сначала...', True, (0,0,0))
textCC = fontCC.render('CleanCom', True, (255,0,0))
textSpace = fontTip.render('Для начала игры нажмите ПРОБЕЛ', True, (0,0,0))
textUp = fontWIN.render('Повышение!', True, (255,0,0))
textPause = fontP.render('Игра приостановлена!', True, (255,0,0))
UnWinX = 77
UnWinY = 10
player_speed = 8
Splayer_x = 10
Splayer_y = 680
color = (161,83,45)
win_rectList=[230,54,129,155,239,151,
    349,151,129,264,239,261,
    349,260,129,372,239,371,
    349,368,129,480,239,480,
    349,480,239,590,349,590
    ]
rectList = [
    118, 197,230, 197,340, 197,
    118, 305,230, 305,340, 305,
    118, 415,230, 415,340, 415,
    118, 520,230, 520,340, 520,
    230, 630,340, 630,
    ]

# Переменные
player_anim_count = 0
player_x = Splayer_x
player_y = Splayer_y
is_jump = False
jump_count= 8.5
jump_h = jump_count
jump_d = -jump_count
gravity=0
gravity0=0
isGravity = False
isDirty =[True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
dCount = 0
wClean = 0
Stimer = 10
timer = Stimer
isGame = True
isGo = False
isWalk = False
win = 0
defeat = 0
isMenu = True
isPause = False

# Изначалное положение грязных окон
for i in range(15):
    r = randint(0, 1)
    if r==0:
        isDirty[i] = False
    else:
        isDirty[i] = True
        dCount += 1
wClean = dCount
dCount = 0


# Главный цикл
running = True
while running:
    keys = pygame.key.get_pressed()

    # Меню
    if isMenu:
        screen.fill((105, 230, 214))
        screen.blit(textCC, (50,200))
        screen.blit(textSpace,(40,350))
        if keys[pygame.K_SPACE]:
            isMenu = False
    else:
        screen.blit(bg,(0,0))


    player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))


    # Пауза
    if not isMenu and isGame:
        if keys[pygame.K_ESCAPE]:
            pygame.time.wait(200)
            if isPause:
                isPause = False
            elif not isPause:
                isPause = True
        if isPause:
            screen.blit(textPause, (135,220))
            isGo = False


    # Мыть окна
    win_rect=[]
    wcollide = []

    # Прямоугольники окон
    for i in range(0,30,2):
        win_rect.append(dirty.get_rect(topleft=(win_rectList[i],win_rectList[i+1])))

    # Столкновение окон с персонажем
    for i in win_rect:
        wcollide.append(pygame.Rect.colliderect(player_rect, i))

    # Мыть окна по кнопке
    for i in range(15):
        if wcollide[i] and keys[pygame.K_q] and isDirty[i] and isGame and not is_jump and not isWalk:
            isDirty[i] = False
            wClean -= 1


    # Картинка грязных окон
    if not isMenu:
        g=0
        for i in range(0,30,2):
            if isDirty[g]:
                if i==0:
                    screen.blit(dirty1,(230,54))
                else:
                    screen.blit(dirty,(win_rectList[i],win_rectList[i+1]))
            g+=1

    # Подоконники
    rect = []
    collide =[]

    # Прямоугольник подоконника
    if not isMenu:
        rect1 = pygame.draw.rect(screen, color, pygame.Rect(230, 120, 65, 10))
        for i in range(0,28,2):
            rect.append(pygame.draw.rect(screen, color, pygame.Rect(rectList[i], rectList[i+1], UnWinX, UnWinY)))

    # Столкновение подоконника с персонажем
    if not isMenu:
        for i in rect:
            collide.append(pygame.Rect.colliderect(player_rect, i))
        collide1 = pygame.Rect.colliderect(player_rect, rect1)

    # Ходить по подоконникам
    if not isMenu:
        if collide1 or collide[0] or collide[1] or collide[2] or collide[3] or collide[4] or collide[5] or collide[6] or collide[7] or collide[8] or collide[9] or collide[10] or collide[11] or collide[12] or collide[13]:
            jump_d = 0
            gravity = 0
        else:
            jump_d = -jump_h

    # Победа
    if wClean == 0:
        if win != 5:
            screen.blit(textWIN, (0,280))
        else:
            screen.blit(textUp, (0,280))
        isGame = False
        if keys[pygame.K_SPACE]:
            Stimer-=0.3
            win+=1
            isGo = False
            player_x = Splayer_x
            player_y = Splayer_y
            for i in range(15):
                r = randint(0, 1)
                if r==0:
                    isDirty[i] = False
                else:
                    isDirty[i] = True
                    dCount += 1
            wClean = dCount
            dCount = 0
            timer = Stimer
            isGame = True

    #Поражение
    elif timer <= 0:
        screen.blit(textDEF, (0,320))
        isGame = False
        if keys[pygame.K_SPACE]:
            Stimer+=0.8
            defeat+=1
            isGo = False
            player_x = Splayer_x
            player_y = Splayer_y
            for i in range(15):
                r = randint(0, 1)
                if r==0:
                    isDirty[i] = False
                else:
                    isDirty[i] = True
                    dCount += 1
            wClean = dCount
            dCount = 0
            timer = Stimer
            isGame = True

    # Счётчик
    if not isMenu:
        counterW = fontCOUNT.render("{:.0f}".format(win), True, (0, 0, 0))
        counterD = fontCOUNT.render("{:.0f}".format(defeat), True, (0, 0, 0))
        screen.blit(counterW, (0, 0))
        screen.blit(counterD, (0, 50))

    # Таймер
    milli = clock.tick()
    seconds = milli / 50.0
    if isGame and isGo:
        timer -= seconds
    timer_text = fontTIME.render("{:.0f}".format(timer), True, (255, 255, 255))
    if isGame and not isMenu:
        screen.blit(timer_text, (370, 690))

    # Анимация
    if not isMenu and not isPause:
        if keys[pygame.K_a] and isGame:
            screen.blit(walk_left[player_anim_count],(player_x,player_y))
        elif isGame:
            screen.blit(walk_right[player_anim_count],(player_x,player_y))

    # Ходьба
    if not isMenu and not isPause:
        if keys[pygame.K_a] and player_x>=0:
            isGo = True
            isWalk = True
            player_x -= player_speed
            if player_anim_count == 1:
                player_anim_count = 0
            else:
                player_anim_count += 1
        elif keys[pygame.K_d] and player_x<=screen_x-38:
            isGo = True
            isWalk = True
            player_x += player_speed
            if player_anim_count == 1:
                player_anim_count = 0
            else:
                player_anim_count += 1
        else:
            isWalk = False

    # Прыжки
    if gravity == 0 and not isPause:
        if not is_jump:
            if keys[pygame.K_w]:
                is_jump = True
                isGo = True
        else:
            if jump_count >= jump_d:
                if jump_count > 0:
                    player_y -= (jump_count ** 2)/2
                else:
                    player_y += (jump_count ** 2)/2
                jump_count -= 1
            else: #конец прыжка
                is_jump = False
                jump_count = jump_h

    # Гравитация
    if not isMenu and not is_jump and not collide1 and not collide[0] and not collide[1] and not collide[2] and not collide[3] and not collide[4] and not collide[5] and not collide[6] and not collide[7] and not collide[8] and not collide[9] and not collide[10] and not collide[11] and not collide[12] and not collide[13]:
        if player_y <=679:
            gravity0 = (jump_count ** 2)/3
            gravity = gravity0 + 0.5
            player_y += gravity
        else:
            gravity=0

    # Ограничение
    if player_y >= 680:
        player_y = 680
    if player_y <= 0:
        player_y = 0

    # Важные команды и выключение игры
    pygame.display.update()
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


