import pygame
import sys
import pygame.sprite as sprite

pygame.init()

# Colors
black = 0,0,0
white = 255,255,255

# Timer
Clock = pygame.time.Clock()

# Frames Per Second
FPS = 60

# Background Image
background = pygame.image.load('background2.png')

background_size = background.get_size()
background_rect = background.get_rect()

# Set screen to background dimentions
screen = pygame.display.set_mode(background_size)

# Player Image
player = pygame.image.load('player.png')

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
sprite_position_y = background_height - (player_height * 1.5)      # Place sprite a couple of pixels above the bottom border of the y-axis

# Sprite Speed and Relative Distance
sprite_pos_enemy = 0.2 
sprite_pos_player = 1.5

sprite_speed_enemy = 0.8
sprite_speed_player = 1

enemy = pygame.image.load('enemy.png')

# Sprite Class
class Sprite(object):  
    def __init__(self, sprite_img, sprite_pos):
        self.image = sprite_img
        # the sprite's position
        self.x = sprite_position_x
        self.y = background_height - (player_height * sprite_pos) 
        self.rect = player_rect

    def movement_keys(self, sprite_speed):
        key = pygame.key.get_pressed()
        dist = 10 # Distance moved in frames

        # if sprite is in the "pathway", moving speed is faster
        if (self.x > 640) or (self.x < 832 ):
            factor_x = 1.5
            factor_y = 1.5
            if key[pygame.K_DOWN]: # down key
                self.y += dist * factor_y * sprite_speed # move down
            elif key[pygame.K_UP]: # up key
                self.y -= dist * factor_y * sprite_speed # move up
            if key[pygame.K_RIGHT]: # right key
                self.x += dist * factor_x * sprite_speed # move right
            elif key[pygame.K_LEFT]: # left key
                self.x -= dist * factor_x * sprite_speed # move left
        # if ((self.x > 0) and (self.x < 192)) or ((self.x > 832) and (self.x < 1024))

        # else if sprite is not in the "pathway", moving speed is noticeable slower
        elif (self.rect.x < 640) or (self.rect.x > 832):
            factor_x = 0
            factor_y = 0
            if key[pygame.K_DOWN]: # down key
                self.y += dist * factor_y # move down
            elif key[pygame.K_UP]: # up key
                self.y -= dist * factor_y # move up
            if key[pygame.K_RIGHT]: # right key
                self.x += dist * factor_x # move right
            elif key[pygame.K_LEFT]: # left key
                self.x -= dist * factor_x# move left

    def draw(self, surface):        
        # blit sprite at current position
        surface.blit(self.image, (self.x, self.y))

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
        message_to_screen("You can move with the arrow keys",white,0)
        message_to_screen("If you keep on the path, you'll run faster",white,50)
        message_to_screen("Press C to begin, Q to quit",white,95.5)

        pygame.display.update()
        Clock.tick(FPS)

sprite1 = Sprite(player, sprite_pos_player)
sprite2 = Sprite(enemy, sprite_pos_enemy)

# Game Loop
def game_loop():
    
    #Variables
    gameExit = False
    gameOver = False

    x = 0
    y = 0

    x1 = 0
    y1 = -background_height

    # while game has not been closed
    while not gameExit:
        # when player has been caught (work in progress)
        while gameOver == True:
            gameDisplay.fill(black)
            message_to_screen("Game over, press C to play again or Q to quit", white,0)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

                    if event.key  == pygame.K_c:
                        gameLoop()
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        # Background Loop        
        y1 += background_speed
        y += background_speed
        screen.blit(background,(x,y))
        screen.blit(background,(x1,y1))
        if y > background_height:
            y = -background_height
        if y1 > background_height:
            y1 = -background_height
        
        # screen.blit(player,(640,664)) # Display static sprite at specified coordinates

        sprite1.movement_keys(sprite_speed_player)
        sprite1.draw(screen) # Draw the sprite into the screen

        sprite2.movement_keys(sprite_speed_enemy)
        sprite2.draw(screen) # Draw the sprite into the screen
        
        pygame.display.flip()
        pygame.display.update()

        Clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()
game_loop()

