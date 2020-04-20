import pygame
import random
import math


# Init PyGame
from pygame import mixer

pygame.init()

# Open screen of the game
screen = pygame.display.set_mode((775, 572))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("background.png")

# Background Sound
#mixer.music.load('background.wav')
#mixer.music.play(-1)

# Player
playerImg = pygame.image.load('baseshipb.ico')
playerX = 370
playerY = 480
playerXchange = 0
playerYchange = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy1.ico'))
    enemyX.append(random.randint(0, 743))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(4)
    enemyYchange.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = 10
bullet_state = "ready"


# SCORE

score_value = 0
textX = 10
textY = 10
font = pygame.font.Font('freesansbold.ttf',32)
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 25:
        return True
    else:
        return False


# Gra
running = True
while running:

    # tło
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # LEFT
            if event.key == pygame.K_LEFT:
                playerXchange = -4
                # RIGHT
            if event.key == pygame.K_RIGHT:
                playerXchange = 4
                # SHOT
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT
                    or event.key == pygame.K_DOWN or event.key == pygame.K_UP):
                playerXchange = 0
                playerYchange = 0

    playerX += playerXchange
    playerY += playerYchange
    # bordering left and right
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 3
            enemyY[i] += enemyYchange[i]

        elif enemyX[i] >= 768:
            enemyXchange[i] = -3
            enemyY[i] += enemyYchange[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            invader_killed = mixer.Sound('invaderkilled.wav')
            invader_killed.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 743)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movment
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
