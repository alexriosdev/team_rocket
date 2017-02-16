import pygame
from utils import vector2
import random

class sprite1:
   # note, no data member declarations needed

   # constructor
   def __init__(self, screen, image, x, y, vx, vy):
      self.screen = screen
      self.image = pygame.image.load(image).convert()
      self.image.set_colorkey((0,0,0))
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.accel = .01
      self.previous = self.position
      self.radius = self.image.get_width()
      

   # method definitions
   def update(self, delta):
       self.previous = self.position
       self.position = self.position.add(self.velocity.scale(pygame.time.get_ticks() - delta))
       self.velocity.y = self.velocity.y + self.accel

       if self.position.y >= self.screen.get_height() - (self.image.get_height() / 2):
           self.position.y = self.screen.get_height() - (self.image.get_height() / 2)
           self.velocity.y = -self.velocity.y

       if self.position.y <= 0 + (self.image.get_height() / 2):
           self.position.y = 0 + (self.image.get_height() / 2)
           self.velocity.y = -self.velocity.y

       if self.position.x >= self.screen.get_width() - self.image.get_width():
           self.position.x = self.screen.get_width() - self.image.get_width()
           self.velocity.x = -self.velocity.x

       if self.position.x <= 0:
           self.position.x = 0
           self.velocity.x = -self.velocity.x

   def draw(self, screen):
       screen.set_colorkey((0,0,0))
       screen.blit( self.image, (self.position.x, self.position.y) )
       

   def collide(self, screen):
       temp = self.velocity.x
       self.velocity.x = self.velocity.y
       self.velocity.y = temp
       pygame.draw.circle(screen, (255,0,0), (int(self.position.x)+self.image.get_width()/2, int(self.position.y)), self.image.get_height() / 2, 4)

   def checkCollision(self, list, screen):
      print self.radius, 1
      for obj in list:
         if self != obj:
            collision = obj.position.subtract(self.position)
            if collision.magnitude() <= obj.radius:
               print collision.magnitude(), obj.radius, "collision"
               obj.position.subtract(collision)
               self.position.subtract(collision.normalized().scale(self.radius*2 - collision.magnitude()))
               obj.collide(screen)         
               
        
   # overload return-this-as-string for printing
   def __str__(self):
      # format allows you to replace "{}" with variable values
      return "({}, {})".format(self.position, self.velocity)

class Player(sprite1):
   def __init__(self, screen, image, x,y, vx,vy):
      self.screen = screen
      screen.set_colorkey((0,0,0))
      self.image = pygame.image.load(image).convert_alpha()
      # self.image.set_colorkey((255,255,255)) #when using convert_alpha, this is not needed
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.rect = pygame.Rect(self.position.x + 15, self.position.y + 15, self.image.get_width() - 70, self.image.get_height()-44)
      self.accel = 1.5
      self.jumping = False
      self.level = self.position.y
      self.gameOver = False
      self.images = [pygame.image.load('c1_new.png').convert_alpha(),pygame.image.load('c2_new.png').convert_alpha(),pygame.image.load('c3_new.png').convert_alpha(), pygame.image.load('c4_new.png').convert_alpha()]
      self.i = 0

   def getPlayerInput(self):
      left = pygame.key.get_pressed()[pygame.K_a]
      right = pygame.key.get_pressed()[pygame.K_d]
      jump = pygame.key.get_pressed()[pygame.K_SPACE]

      return (left, right, jump)

   def jump(self):
      self.jumping = True
      self.velocity.y = -20
      self.position.y += .01
      self.level += .01

   def draw(self, screen):
      screen.set_colorkey((0,0,0))
      screen.blit( self.image, (self.position.x, self.position.y))
      if not self.jumping:
         self.image = self.images[int(self.i)]

   def update(self, delta):
      print
      self.rect.y = self.position.y + 40
      self.rect.x = self.position.x + 35
      self.i = ((self.i +.17) % 100) %2
      
      # Get user inputs
      controls = self.getPlayerInput()

      # Distance in frames
      dist = 15

      # Move Left
      if controls[0] == 1 and controls[1] == 0 and controls[2] == 0 and self.jumping != True:
         self.position.x = self.position.x - dist
         print self.position.x
      
      # Move Right
      elif controls[0] == 0 and controls[1] == 1 and controls[2] == 0 and self.jumping != True:
         self.position.x = self.position.x + dist
         print self.position.x

      # Jump
      elif controls[0] == 0 and controls[1] == 0 and controls[2] == 1 and self.jumping != True:
         self.jump()

      # The Code Below adds fluidity to the Jump:

      # Move Left + Jump
      elif controls[0] == 1 and controls[1] == 0 and controls[2] == 1 and self.jumping != True:
         self.jump()
         self.position.x = self.position.x - dist

      # Move Right + Jump
      elif controls[0] == 0 and controls[1] == 1 and controls[2] == 1 and self.jumping != True:
         self.jump()
         self.position.x = self.position.x + dist

      # After Jumping, Fall Left
      elif controls[0] == 1 and controls[1] == 0 or controls[2] == 1 and self.jumping != True:
         self.position.x = self.position.x - dist

      # After Jumping, Fall Right
      elif controls[0] == 0 and controls[1] == 1 or controls[2] == 1 and self.jumping != True:
         self.position.x = self.position.x + dist

      # Update physics
      if self.jumping:
         self.position = self.position.add(self.velocity.scale((pygame.time.get_ticks()* .25) - delta ))
         print self.position
         self.velocity.y = self.velocity.y + self.accel
         if self.position.y >= self.level:
            self.velocity.y = 0
            self.position.y = self.level
            self.jumping = False
            
      # Keep sprite in boundaries
      if self.position.y >= self.screen.get_height() - self.image.get_width()/2:
         print "GAME OVER"
         self.gameOver = True

      if self.position.y <= 0 :          
         self.position.y = 0 

      if self.position.x >= self.screen.get_width() - self.image.get_width():
         self.position.x = self.screen.get_width() - self.image.get_width()
         self.velocity.x = -self.velocity.x

      if self.position.x <= 0:
         self.position.x = 0
         self.velocity.x = -self.velocity.x

   def checkCollision(self, list, screen):
      for obj in list:
         if obj != self:
            obj.checkCollision(self, screen)

         else:
            if (self.position.x <= 118 or self.position.x >= 778) and not self.jumping:
               print "out of bounds"
               self.position.y = self.position.y + 1
               self.level = self.level + 1
            return self.gameOver
      
            

# Enemy only mimics player movements
class Enemy(sprite1):
   def __init__(self, screen, image, x,y, vx,vy):
      self.screen = screen
      self.image = pygame.image.load(image).convert()
      self.image.set_colorkey((255,255,255))
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.accel = 1
      self.jumping = False

      self.rect = pygame.Rect(self.position.x + 15, self.position.y + 15, self.image.get_width() - 70, self.image.get_height()-50)
      self.clip = pygame.Rect( 0, 0, 160, 180 )
      self.images = [pygame.image.load('security1.png').convert_alpha(),pygame.image.load('security2.png').convert_alpha()]
      self.i = 0

  
   def getPlayerInput(self):
      left = pygame.key.get_pressed()[pygame.K_a]
      right = pygame.key.get_pressed()[pygame.K_d]
      jump = pygame.key.get_pressed()[pygame.K_SPACE]

      return (left, right, jump)

   def jump(self):
      self.jumping = True
      self.velocity.y = self.velocity.y - 5

   def draw(self, screen):
      screen.set_colorkey((0,0,0))
      screen.blit( self.image, (self.position.x, self.position.y))
      if not self.jumping:
         self.image = self.images[int(self.i)]

   def update(self, delta):
      self.rect.y = self.position.y + 40
      self.rect.x = self.position.x + 30
      self.i = ((self.i +.15) % 100) %2

      #get Input
      controls = self.getPlayerInput()

      # Distance in frames
      dist = 15

      if controls[0] == 1 and controls[1] == 0 and controls[2] == 0 and self.jumping != True:
         self.position.x = self.position.x - dist
         print self.position.x

      elif controls[0] == 0 and controls[1] == 1 and controls[2] == 0 and self.jumping != True:
         self.position.x = self.position.x + dist
         print self.position.x

      elif controls[0] == 0 and controls[1] == 0 and controls[2] == 1 and self.jumping != True:
         self.jump()

      # The Code Below adds fluidity to the Jump:

      # Move Left + Jump
      elif controls[0] == 1 and controls[1] == 0 and controls[2] == 1 and self.jumping != True:
         self.jump()
         self.position.x = self.position.x - dist

      # Move Right + Jump
      elif controls[0] == 0 and controls[1] == 1 and controls[2] == 1 and self.jumping != True:
         self.jump()
         self.position.x = self.position.x + dist

      # After Jumping, Fall Left
      elif controls[0] == 1 and controls[1] == 0 or controls[2] == 1 and self.jumping != True:
         self.position.x = self.position.x - dist

      # After Jumping, Fall Right
      elif controls[0] == 0 and controls[1] == 1 or controls[2] == 1 and self.jumping != True:
         self.position.x = self.position.x + dist

      # update physics
      if self.jumping:
         #self.previous = self.position
         self.position = self.position.add(self.velocity.scale((pygame.time.get_ticks()* .25) - delta ))
         print self.position
         self.velocity.y = self.velocity.y + self.accel
         #if self.position.y >= 768-280:
         if self.position.y >= self.screen.get_height() - (self.image.get_height() / 2):
            self.velocity.y = 0
            self.jumping = False     
      
      # Keep sprite in boundaries
      if self.position.y >= self.screen.get_height() - (self.image.get_height() / 2):
         self.position.y = self.screen.get_height() - (self.image.get_height() / 2)
         self.velocity.y = -self.velocity.y

      if self.position.y <= 0 + (self.image.get_height() / 2):
         self.position.y = 0 + (self.image.get_height() / 2)      
         self.velocity.y = -self.velocity.y

      if self.position.x >= self.screen.get_width() - self.image.get_width():
         self.position.x = self.screen.get_width() - self.image.get_width()
         self.velocity.x = -self.velocity.x

      if self.position.x <= 0:
         self.position.x = 0
         self.velocity.x = -self.velocity.x

   def checkCollision(self, list, screen):
      return True

# Pothole simple red rectangle for now
class Pothole(sprite1):
   def __init__(self, screen, image, x, y, vx, vy):
      self.screen = screen
      self.image = pygame.image.load(image).convert()
      self.image.set_colorkey((255,255,255))
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.rect = pygame.Rect(self.position.x , self.position.y, self.image.get_width(), self.image.get_height())
      self.accel = .1

      
   def update(self, delta):
      self.position.y = delta % 768
      self.rect.y = self.position.y

   def checkCollision(self, list, screen):
      return True

   def checkCollision(self, player, screen):
        if (self.rect.colliderect(player.rect) and not player.jumping):
               print "colission", self.rect.x, player.rect.x
               player.level = player.level+10
               player.position.y += 10
               screen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
               if player.gameOver:
                  return True
               return False

# Student obstacle
class Students(sprite1):
   def __init__(self, screen, image, x,y, vx,vy,accel):
      self.screen = screen
      self.image = pygame.image.load(image).convert()
      self.image.set_colorkey((255,255,255))
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.rect = pygame.Rect(self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
      self.accel = accel # Determines the rate at which sprite falls down
      self.previous = self.position
      self.radius = self.image.get_width()

      self.velocity.y = self.velocity.y + 5

      self.rect = pygame.Rect(self.position.x + 30  , self.position.y, self.image.get_width() - 68, self.image.get_height())
      self.clip = pygame.Rect( 0, 0, 160, 180 )
      self.images = [pygame.image.load('s1_new.png').convert_alpha(),pygame.image.load('s2_new.png').convert_alpha(),pygame.image.load('s3_new.png').convert_alpha(), pygame.image.load('s4_new.png').convert_alpha()]
      self.i = 0


   def draw(self, screen):
      screen.set_colorkey((0,0,0))
      screen.blit( self.image, (self.position.x, self.position.y))
      self.image = self.images[int(self.i)]

   def update(self, delta):
      self.rect.y = self.position.y
      self.rect.x = self.position.x + 30

      self.i = ((self.i +.14) % 100) %2
      
      # Simulates Falling/Walking down
      self.position.y = self.position.y + (self.velocity.y * self.accel)
      if self.position.y >= self.screen.get_height() - self.image.get_height():
         self.position.y = random.randrange(-382,0) # sprite appears in a random spot in the y-axis, occurs offscreen as to give space for its next iteration
         self.position.x = random.randint(192, 832) # sprite appears in a random spot in the x-axis, along the walking pathway

      if self.position.y > 0:
         self.velocity.y = self.screen.get_height() - (self.image.get_height() / 2)

   def checkCollision(self, list, screen):
      return True
   
   def checkCollision(self, player, screen):
         if (self.rect.colliderect(player.rect)):
               print "student colission"
               player.level = player.level+10
               player.position.y += 10
               screen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
               if player.gameOver:
                  return True
               return False
      




