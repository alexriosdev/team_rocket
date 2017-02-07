import pygame
import sys
from utils import vector2
from sprite1 import *

pygame.init()
pygame.display.set_caption( "Run Bronco Run!" ) #Placeholder name

# Colors
black = 0,0,0
white = 255,255,255

# Timer
Clock = pygame.time.Clock()

# Frames Per Second
FPS = 60

# Background Image
background = pygame.image.load('background_update.png')

background_size = background.get_size()
background_rect = background.get_rect()

# Set screen to background dimentions
screen = pygame.display.set_mode(background_size)

# Player Image
player = pygame.image.load('character.png')

player_size = player.get_size()
player_rect = player.get_rect()

player_width, player_height = player_size

# Get background width and height dimentions
background_width, background_height = background_size
x = 0
y = 0

# Second set of x and y used for moving background
x1 = 0
y1 = -background_height

# Determines how fast the background moves, in frames
background_speed = 10

# Sprite Position
sprite_position_x = (background_width / 2) - (player_width / 2)    # Place sprite in the center of x-axis
sprite_position_y = background_height - (player_height * 1.8)      # Place sprite a couple of pixels above the bottom border of the y-axis

# Sprite Speed and Relative Position
sprite_pos_enemy = 0.2 
sprite_pos_player = 1.5

# Part of Old Code
# sprite_speed_enemy = 0.8
# sprite_speed_player = 1

enemy = pygame.image.load('enemy.png')
enemy_sprite_position_y = background_height - (player_height * sprite_pos_enemy) 

font = pygame.font.SysFont(None, 25)

# Message-to-screen Function
def message_to_screen(msg,color,y):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(background_width/2, (background_height/2) + y))
    # screen.blit(screen_text, [background_width/2, y])
    screen.blit(text, text_rect)

# Start Screen 
def game_intro():
    
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        screen.fill(black)        
        message_to_screen("Welcome",white,-95.5)
        message_to_screen("The objective of this game is to escape the law",white,-50)
        message_to_screen("Use A to move left, D to move right",white,0)
        message_to_screen("Use Spacebar to jump",white,50)
        message_to_screen("Press C to continue, Q to quit",white,95.5)

        pygame.display.update()
        Clock.tick(FPS)

# Player(self, screen, image, x, y, vx, vy, y_len)
#list = [Pothole(screen, 195, 50, 0, 0),
#        Enemy( screen, "enemy.png", sprite_position_x, enemy_sprite_position_y, 0, 1),
#        Player( screen, "character.png", sprite_position_x, sprite_position_y, 0, 1)
#       ]
 

# Game Loop
def game_loop():
    
    # Variables
    gameExit = False
    gameOver = False

    x = 0
    y = 0

    x1 = 0
    y1 = -background_height

    time = pygame.time.get_ticks()

    # Player(self, screen, image, x, y, vx, vy, y_len)
    list = [Pothole(screen, 195, 50, 0, 0),
            Enemy( screen, "enemy.png", sprite_position_x, enemy_sprite_position_y, 0, 1),
            Player( screen, "character.png", sprite_position_x, sprite_position_y, 0, 1)
           ]

    # while game has not been closed
    while not gameExit:
        # when player has been caught (work in progress)
        while gameOver == True:
            screen.fill(black)
            message_to_screen("Game over, press C to play again or Escape key to quit", white,0)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameExit = True
                        gameOver = False

                    if event.key  == pygame.K_c:
                        game_loop()
                        
        # Exit Game by pressing the Escape Key            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                #sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                gameExit = True
                # gameOver = False
                pygame.quit()
                sys.exit()


        # Background Loop        
        y1 += background_speed
        y += background_speed
        screen.blit(background,(x,y))
        screen.blit(background,(x1,y1))
        if y > background_height:
            y = -background_height
        if y1 > background_height:
            y1 = -background_height
        
        for obj in list:
            obj.update(time)
            time = pygame.time.get_ticks() * .25
           
        gameOver = obj.checkCollision(list, screen)
        
        for obj in list:
            obj.draw(screen)
        
        pygame.display.flip()
        pygame.display.update()

        Clock.tick(FPS)

    pygame.quit()   
    quit()
    
game_intro()
game_loop()

