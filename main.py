import pygame
from pygame import mixer
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background1.jpg')

mixer.music.load('bgm.wav')
mixer.music.play(-1)

pygame.display.set_caption("Destroy the Dementors")
icon = pygame.image.load('hpseeker.png ')
pygame.display.set_icon(icon)
playerImg = pygame.image.load('hpseeker.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('dementor.png'))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(30)

spellImg = pygame.image.load('magicwand.png')
spellX = 0
spellY = 480
spellX_change = 0.5
spellY_change = 4
spell_state = 'ready'
score_value: int = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER ", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))





def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def wave_spell(x, y):
    global spell_state
    spell_state = "wave"
    screen.blit(spellImg, (x + 5, y + 10))


def collision(enemyX, enemyY, spellX, spellY):
    distance = math.sqrt(math.pow(enemyX - spellX, 2) + math.pow(enemyY - spellY, 2))
    if distance <= 27:
        return True
    else:
        return False


# LOOP FOR THE GAME
running = True
while running:
    screen.fill((0, 255, 255))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                spell_sound = mixer.Sound('spell.wav')
                spell_sound.play()
                spellX = playerX
                wave_spell(spellX, spellY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX[i] = 0.3
            enemyY[i] += enemyY_change[i]

        collise = collision(enemyX[i], enemyY[i], spellX, spellY)
        if collise:
            explode_sound = mixer.Sound('firework.wav')
            explode_sound.play()
            spellY = 480
            spell_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)



    if spellY <= 0:
        spellY = 480
        spell_state = "ready"
    if spell_state is "wave":
        wave_spell(spellX, spellY)
        spellY -= spellY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
