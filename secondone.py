import random
import pygame
import math
from pygame import mixer

# initialise pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))        # across right (0,0) ---> top right (800,0)
                                                    # moving down (0,0) ---> bottom left (0,600) | bottom right (800,600)
# background
bg_image = pygame.image.load('purplespace.jpg')

# bgm
mixer.music.load('bgm.wav')
mixer.music.play(-1)                            # play bgm on loop

# icon
pygame.display.set_caption("Space Attack")
icon = pygame.image.load('spaceicon.png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('rocket.png')
playerX = 370
playerY = 480                                   # player's initial position. X and Y coordinate
playerX_change = 0                              # create X's temp position to move left and right

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 6                                         # number of enemies
for i in range(num):                                    # iterates enemies back to position after it gets shot
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))               # places enemy in 0<X<736 moving right and left
    enemyY.append(random.randint(50, 150))              #places enemy in 50<Y<150 within 0<X<736
    enemyX_change.append(0.3)                           # starts moving right
    enemyY_change.append(40)                            # moving down by Y=40

# bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0                                             # bullet doesnt move along sides
bulletY = 480                                           # bullet moves up
bulletX_change = 0                                      # bullet doesnt move along sides
bulletY_change = 5                                      # bullet's speed moving up (Yaxis)
bullet_state = "ready"                                  #bullet is ready in its position

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 16)
textx = 10
texty = 10                                              # position of score (10,10)

# game over text
over_font1 = pygame.font.Font('schoolfont.ttf', 32)         #one for GAMEOVER
over_font2 = pygame.font.Font('freesansbold.ttf', 16)       #for your score:


def show_score(x, y):
    score_value = font.render("Score : " + str(score), True, (102, 102, 0))
    screen.blit(score_value, (x, y))                                            #writes score on screen


def game_over():
    game_text1 = over_font1.render("GAME OVER!", True, (255, 255, 255))
    game_text2 = over_font2.render("Your Score : " + str(score), True, (204, 204, 0))
    screen.blit(game_text1, (200, 250))
    screen.blit(game_text2, (350, 350))                                         #writes final score on screen


def player(x, y):
    screen.blit(player_img, (x, y))                                 # draws player on screen


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))                               # draws enemy on screen


def fire_bullet(x, y):
    global bullet_state                                         # bullet_score=ready
    bullet_state = "fire"                                       #Now FIRE!!!
    screen.blit(bullet_img, (x + 16, y + 10))                   #bullet fires from player's center tip (+16,+10)


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))) # collision method
    if distance < 27:                                           #
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(bg_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # bullet shoot
                    bullet_sound = mixer.Sound('bulletsound.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num):

        # game over
        if enemyY[i] > 440:
            for j in range(num):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        coll = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if coll:
            alien_sound = mixer.Sound('aliensound.wav')
            alien_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # BUllet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textx, texty)
    pygame.display.update()
