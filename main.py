import pygame
import random
import math
import time
from pygame import mixer
from pygame.locals import *

# initialize pygame
pygame.init()
# screen
screen = pygame.display.set_mode((800, 600))

start = time.time()  # the variable that holds the starting time
elapsed = 20+ start

# the variable that holds the number of seconds elapsed.
# while elapsed < 300:         #while less than 30 seconds have elapsed
#   elapsed = time.time() - start
# TITLE
pygame.display.set_caption("the cat")
icon = pygame.image.load("happy.png")
pygame.display.set_icon(icon)
# background
background = pygame.image.load("background.jpg")
# background sound
mixer.music.load("bensound-psychedelic.mp3")
mixer.music.play(-1)
# player
player = pygame.image.load("cat (2).png")
playerx = 400
playery = 530
playerx_change = 0
playery_change = 0

# enemy
enemy = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
enemy_number = 6
for i in range(enemy_number):
    enemy.append(pygame.image.load("witch.png"))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(0.2)
    enemyy_change.append(40)

# bullet
bullet = pygame.image.load("lighting.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 0.7
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# time
timex = 170
timey = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
    game_over_s = over_font.render("GAME OVER", True, (102, 40, 65))
    screen.blit(game_over_s, (200, 300))


def show_score(x, y):
    score_screen = font.render("score :" + str(score), True, (102, 40, 65))
    screen.blit(score_screen, (x, y))


def time_left(x, y):
    global elapsed
    time_left = font.render("time:" + str(int(elapsed - time.time())), True, (102, 40, 65))
    screen.blit(time_left, (x, y))


def playerz(x, y):
    screen.blit(player, (x, y))


def enemyz(x, y, i):
    screen.blit(enemy[i], (x, y))


def fire_bullet(x, y):
    screen.blit(bullet, (x + 20, y))


def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True


# game loop
running = True
flg = 0
while (running):
    screen.fill((102, 40, 65))
    screen.blit(background, (0, 0))
    if ((elapsed - time.time()) <= 0):
        game_over()
        pygame.display.update()
        flg = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -1
            if event.key == pygame.K_RIGHT:
                playerx_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("mixkit-big-fire-magic-swoosh-1327.wav")
                    bullet_sound.play()
                    # get x coordinates of the cat
                    bulletx = playerx
                    bullet_state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                playerx_change = 0

    # screen updates

    # player boundary
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    if playerx >= 743:
        playerx = 743

    # enemy movement
    if flg == 0:
        for i in range(enemy_number):
            if enemyy[i] > 400:
                for j in range(enemy_number):
                    enemyy[j] = 2000

                game_over()
                break

            enemyx[i] += enemyx_change[i]
            if enemyx[i] <= 0:
                enemyx_change[i] = 0.2
                enemyy[i] += enemyy_change[i]
            if enemyx[i] >= 736:
                enemyx_change[i] = -0.2
                enemyy[i] += enemyy_change[i]
                # collision

            iscollison = collision(enemyx[i], enemyy[i], bulletx, bullety)
            if iscollison:
                bullet_sound = mixer.Sound("mixkit-digital-cartoon-falling-405.wav")
                bullet_sound.play()
                bullety = 480
                bullet_state = "ready"
                score += 1
                enemyx[i] = random.randint(0, 735)
                enemyy[i] = random.randint(50, 150)

        # bullet movement
        if bullety <= 0:
            bullety = 500
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletx, bullety)
            bullety -= bullety_change
        for i in range(enemy_number):
            enemyz(enemyx[i], enemyy[i], i)
        playerz(playerx, playery)
        show_score(textx, texty)
        time_left(timex, timey)

    pygame.display.update()
