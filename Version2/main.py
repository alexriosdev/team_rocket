#Huriel Hernandez
import pygame
import sys
from utils import vector2
from sprite1 import *

# setup
pygame.init()
screen = pygame.display.set_mode( (1024, 768) )
pygame.display.set_caption( "Campus Escape" )

background = pygame.image.load("background.jpg").convert()

screen.blit(background, (0,0))

list = [Player( screen, "character.jpg", 310, 768-280, 0, 1)]
t = pygame.time.get_ticks()
y = 0
z = 0

while True:

    #get user events
    pygame.event.pump()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    #update
    #rotate = pygame.transform.rotate(background,z *.025)
    screen.blit(background, (0,y-768))
    screen.blit(background, (0,y))
    y = (t) % 768
    z = (t) 
  
    
    for obj in list:
        obj.update(t)
      
        t = pygame.time.get_ticks() * .25
        #obj.checkCollision(list, screen)

        
    
    #rende 
    
    for obj in list:
        obj.draw(screen)
        
    pygame.display.flip()


 


 
