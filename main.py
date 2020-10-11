import pygame
import math
import random
from pygame import mixer

# To Initialize the game
pygame.init()

# To initialize the game window , Caption, Icon
screen = pygame.display.set_mode(size=(800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Screen Background
backgroundImg = pygame.image.load("gameBackground.jpg")
backgroundImg = pygame.transform.scale(backgroundImg, (800, 600))

# Player Details
playerImg = pygame.image.load("playerimageicon.png")
playerImg = pygame.transform.scale(playerImg, (55, 50))
playerXPos = 370
playerYPos = 540
pxPos_change = 0


def player(xpos, ypos):
    screen.blit(playerImg, (xpos, ypos))


# Enemy Details
enemyImg = []
enemyXPos = []
enemyYPos = []
exPos_change = []
eyPos_change = []
enemy_forward = []
numberOfEnemy = 10
espeed = 0

for i in range(numberOfEnemy):
    enemyImg.append(pygame.image.load('enemy1.png'))
    enemyXPos.append(random.randint(0, 736))
    enemyYPos.append(random.randint(50, 150))
    exPos_change.append(3)
    eyPos_change.append(40)


def enemy(xpos, ypos, i):
    screen.blit(enemyImg[i], (xpos, ypos))

def checkEmenySpeed(score):
    if score < 10:
        return 0
    elif score >= 10 and score < 40:
        return 0.8
    elif score >= 40 and score < 80:
        return 1.6
    elif score >= 80 and score < 120:
        return 2.4
    elif score >= 120 and score < 160:
        return 3.2
    elif score >= 160 and score < 180:
        return 4.0
    else:
        return 4.8

# Bullet Details
bulletImg = pygame.image.load("bullet.png")
bulletXPos = 0
bulletYPos = 540
bulletxPos_change = 0
bulletyPos_change = 10
bullet_State = False


def bullet(xpos, ypos):
    global bullet_State
    bullet_State = True
    screen.blit(bulletImg, (xpos, ypos))

def isCollision(x2, x1, y2, y1):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 30:
        return True
    return False

# SCORE

pScore = 0
font = pygame.font.Font("freesansbold.ttf", 24)
scoreXPos = 10
scoreYPos = 10

def showScore(x, y):
    score = font.render("Score : " + str(pScore), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOver():
    overFont = pygame.font.Font("freesansbold.ttf", 60)
    x = 230
    y = 200
    overScore = overFont.render("Score : " + str(pScore), True, (255, 255, 255))
    gameover = overFont.render("Game Over", True, (255, 255, 255))
    screen.blit(gameover,  (x, y))
    screen.blit(overScore, (x + 50, y + 80))






# Game main loop
RUNNING = True
while RUNNING:
    screen.fill((13, 207, 226))  # Background Color
    screen.blit(backgroundImg, (0, 0))  # Background Image
    showScore(scoreXPos, scoreYPos)   # Show Score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit button event
            RUNNING = False

        if event.type == pygame.KEYDOWN:  # Player Movement
            if event.key == pygame.K_LEFT:
                pxPos_change = -5
            if event.key == pygame.K_RIGHT:
                pxPos_change = 5
            if event.key == pygame.K_SPACE:
                if not bullet_State:
                    mixer.music.load("bulletShot.wav")
                    mixer.music.play(1)
                    bulletXPos = playerXPos + 16
                    bullet(bulletXPos, bulletYPos - 15)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pxPos_change = 0

    # Spaceship Movement
    playerXPos += pxPos_change
    if playerXPos <= 0:
        playerXPos = 0
    elif playerXPos >= 745:
        playerXPos = 745
    player(playerXPos, playerYPos)

    # Enemy Movement
    for i in range(numberOfEnemy):
        espeed = 0 # checkEmenySpeed(pScore)
        enemyXPos[i] += exPos_change[i]
        if enemyXPos[i] >= 768 and enemyYPos[i] <= 500:
            enemyYPos[i] += 30
            exPos_change[i] = -2 - espeed
        elif enemyXPos[i] <= 0 and enemyYPos[i] <= 500:
            enemyYPos[i] += 30
            exPos_change[i] = 2 + espeed
        elif enemyYPos[i] >= 500:
            gameOver()
            RUNNING = False

        # Check Collision
        collide = isCollision(enemyXPos[i], bulletXPos, enemyYPos[i], bulletYPos)
        if collide:
            mixer.music.load("enemyKill.wav")
            mixer.music.play(1)
            bulletYPos = 540
            bullet_State = False;
            pScore += 1
            enemyXPos[i] = random.randint(0, 768)
            enemyYPos[i] = random.randint(0, 200)

        enemy(enemyXPos[i], enemyYPos[i], i)

    # Bullet Movement
    if bulletYPos <= -20:
        bulletYPos = 540
        bullet_State = False;
    if bullet_State:
        bulletYPos -= bulletyPos_change
        bullet(bulletXPos, bulletYPos)
    pygame.display.update()

pygame.time.wait(5000)
