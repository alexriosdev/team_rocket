import pygame
import sys
import random
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
background = pygame.image.load('Images/background_update.png')

background_size = background.get_size()
background_rect = background.get_rect()

# Background Music
pygame.mixer.music.load('Sounds/song.mp3')

# Set screen to background dimentions
screen = pygame.display.set_mode(background_size)

# Player Image
player = pygame.image.load('Images/player1.png')

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
sprite_position_y = sprite_position_x      # Place sprite a couple of pixels above the bottom border of the y-axis

# Sprite Speed and Relative Position
sprite_pos_enemy = 0.2 
sprite_pos_player = 1.5

enemy = pygame.image.load('Images/security1.png')
enemy_sprite_position_y = background_height - (player_height * sprite_pos_enemy) 

font = pygame.font.SysFont(None, 25)

# Message-to-screen Function
def message_to_screen(msg,color,y):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(background_width/2, (background_height/2) + y))
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
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        screen.fill(black)        
        message_to_screen("Welcome",white,-95.5)
        message_to_screen("The objective of this game is to escape the law",white,-50)
        message_to_screen("Use A to move left, D to move right",white,0)
        message_to_screen("Use Spacebar to jump",white,50)
        message_to_screen("Press Spacebar to continue, Q to quit",white,95.5)

        pygame.display.update()
        Clock.tick(FPS)   

# Game Loop
def game_loop():
    score = 0

    # Background Music Volume
    pygame.mixer.music.set_volume(.4)
    pygame.mixer.music.play(-1, 0)
    
    # Variables
    gameExit = False
    gameOver = False

    x = 0
    y = 0

    x1 = 0
    y1 = -background_height
    
    time = pygame.time.get_ticks()

    list = [
            Enemy( screen, "Images/security1.png", sprite_position_x, enemy_sprite_position_y, 0, 1),
            Player( screen, "Images/player1.png", sprite_position_x, sprite_position_y, 0, 1)
           ]

    # while game has not been closed
    while not gameExit:
        # when player has been caught (work in progress)
        while gameOver == True:
            screen.fill(black)
            message_to_screen("SCORE: " + str(score), white, -40)
            message_to_screen("Game over, press Spacebar to play again or Escape key to quit", white,0)
            pygame.display.update()
            pygame.init()
            hi_file_r.close() # End reading file

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameExit = True
                        gameOver = False

                    if event.key  == pygame.K_SPACE:
                        hi_file_w = open("highscore.txt","w")
                        hi_file_w.write(str(score)) # Store highscore in file
                        hi_file_w.close() # End writing file                        
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

        # Object Spawning and Spawning Interval
        if int(score) % 500 == 0:
            student =  Students( screen, "Images/student1.png", random.randint(192, 832), random.randint(0, 191), 0, 1, random.uniform(0.03, .01))
            list.insert(0,student)

        if int(score) % 900 == 0:
            powerup =  Powerup( screen, "Images/coffee1.png", random.randint(192, 832), random.randint(-382, 0), 0, 1, random.uniform(0.03, .01))
            list.insert(0,powerup)

        # Default y-interval for objects was random.randint(-381,0)
        if int(score) % 79 == 0:            
            trash =  Obstacle( screen, "Images/trash1.png", random.randint(192, (832-90)), random.randint(-191, 0), 0, 1, 0.01)
            list.insert(0,trash)

        if int(score) % 113 == 0:            
            bench1 =  Obstacle( screen, "Images/bench1.png", random.randint(192, (832-281)), random.randint(-382, -191), 0, 1, 0.01)
            list.insert(0,bench1)

        if int(score) % 187 == 0:            
            bench2 =  Obstacle( screen, "Images/bench3.png", random.randint(192, (832-562)), random.randint(-764, -382), 0, 1, 0.01)
            list.insert(0,bench2)
            
        if int(score) % 223 == 0:            
            bench3 =  Obstacle( screen, "Images/bench4.png", random.randint(0, (1024-843)), random.randint(-764, -382), 0, 1, 0.01)
            list.insert(0,bench3)
            
        for obj in list:
            obj.update(time)
            time = pygame.time.get_ticks() * .25
            
        gameOver = obj.checkCollision(list, screen)

        # Get Coordinates for Enemy Sprite
        coordinates = obj.position
        list[-2].updateCoordinates(coordinates)
      
        # Draw objects in list
        for obj in list:
            obj.draw(screen)

        score = score + 1

        # Display Current Score
        basicfont = pygame.font.SysFont(None, 48)
        text = basicfont.render("score: " + str(score) , True, (255, 255, 255))
        screen.blit(text, (8,4))

        # Display Previous Score
        hi_file_r = open("highscore.txt","r") # read file
        text = basicfont.render("prev: " + hi_file_r.read(), True, (255, 255, 255))
        screen.blit(text, (832,4))
        hi_file_r.close() # close file
                    
        pygame.display.flip()
        pygame.display.update()

        #int(time * 4  / 1000))

        Clock.tick(FPS)

    pygame.quit()   
    quit()
    
game_intro()
game_loop()

