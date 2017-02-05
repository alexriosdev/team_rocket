import pygame
import sys
import pygame.sprite as sprite

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

# Sprite Class
class Sprite(object):  
    def __init__(self):
        self.image = player
        # the sprite's position
        self.x = (background_width / 2) - (player_width / 2)    # Place sprite in the center of x-axis
        self.y = background_height - (player_height * 1.5)      # Place sprite a couple of pixels above the bottom border of the y-axis
        self.rect = player_rect

    def movement_keys(self):
        key = pygame.key.get_pressed()
        dist = 10 # Distance moved in frames

        # if sprite is in the "pathway", moving speed is faster
        if (self.x > 640) or (self.x < 832 ):
            factor_x = 1.5
            factor_y = 1.5
            if key[pygame.K_DOWN]: # down key
                self.y += dist * factor_y # move down
            elif key[pygame.K_UP]: # up key
                self.y -= dist * factor_y # move up
            if key[pygame.K_RIGHT]: # right key
                self.x += dist * factor_x # move right
            elif key[pygame.K_LEFT]: # left key
                self.x -= dist * factor_x# move left
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

sprite1 = Sprite()

running = True

# Game Loop
while running:
    screen.blit(background,background_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    sprite1.movement_keys()
    sprite1.draw(screen) # Draw the sprite into the screen
    
    pygame.display.flip()
    pygame.display.update()

    Clock.tick(FPS)
