import pygame
from utils import vector2

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
       #pygame.draw.rect(screen, (0,0,255),(self.position.x -20  , self.position.y-200, self.image.get_width() + 40, self.image.get_width() + 20),0)
       #pygame.draw.circle(screen, (255,255,255), (int(self.position.x)+self.image.get_width()/2, int(self.position.y)), self.image.get_width() / 2, 1)
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
               #obj.position.subtract(collision.normalized().scale(self.radius*2 - collision.magnitude()))
               self.position.subtract(collision.normalized().scale(self.radius*2 - collision.magnitude()))
               obj.collide(screen)         
               
        
   # overload return-this-as-string for printing
   def __str__(self):
      # format allows you to replace "{}" with variable values
      return "({}, {})".format(self.position, self.velocity)



class Player(sprite1):
   def __init__(self, screen, image, x,y, vx,vy):
      self.screen = screen
      self.image = pygame.image.load(image).convert()
      self.image.set_colorkey((255,255,255))
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.accel = 1.5
      self.previous = self.position
      self.radius = self.image.get_width()
      self.jumping = False
      self.level = self.position.x
      self.gameOver = False

   def getPlayerInput(self):
      left = pygame.key.get_pressed()[pygame.K_a]
      right = pygame.key.get_pressed()[pygame.K_d]
      jump = pygame.key.get_pressed()[pygame.K_SPACE]

      return (left, right, jump)

   def jump(self):
      self.jumping = True
      self.velocity.y = -20 

   def update(self, delta):
      print
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
         #self.previous = self.position
         self.position = self.position.add(self.velocity.scale((pygame.time.get_ticks()* .25) - delta ))
         print self.position
         self.velocity.y = self.velocity.y + self.accel
         #if self.position.y >= 768-280:
         if self.position.y >= self.level:
            self.velocity.y = 0
            self.position.y = self.level
            self.jumping = False
            
      # Keep sprite in boundaries
      if self.position.y >= self.screen.get_height() - self.image.get_width()/2:
         #self.position.y = self.screen.get_height() - self.image.get_width()/2
         #self.velocity.y = -self.velocity.y 
         print "GAME OVER"
         #gameDisplay.fill(black)
         self.gameOver = True

      if self.position.y <= 0 :          
         self.position.y = 0 
         #self.velocity.y = -self.velocity.y
         #print "b"

      if self.position.x >= self.screen.get_width() - self.image.get_width():
         self.position.x = self.screen.get_width() - self.image.get_width()
         self.velocity.x = -self.velocity.x

      if self.position.x <= 0:
         self.position.x = 0
         self.velocity.x = -self.velocity.x

   def checkCollision(self, list, screen):
      print self.position.x
      for obj in list:
         if obj != self:
            if self.position.y >= obj.position.y and self.position.y <= obj.position.y + 40 and not self.jumping or self.position.y + self.image.get_height() >= obj.position.y and self.position.y + self.image.get_height() <= obj.position.y + 40 and not self.jumping:
               print "colission"
               self.level = self.level+10
               self.position.y += 10
               screen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
               if self.gameOver:
                  return True
               return False
         else:
            if (self.position.x <= 118 or self.position.x >= 778) and not self.jumping:
               print "out of bounds"
               self.position.y = self.position.y + 1
               self.level = self.level + 1






# Enemy only mimics player movements
class Enemy(sprite1):
   def __init__(self, screen, image, x,y, vx,vy):
      self.screen = screen
      self.image = pygame.image.load(image).convert()
      self.image.set_colorkey((255,255,255))
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.accel = 1
      self.previous = self.position
      self.radius = self.image.get_width()
      self.jumping = False
  
   def getPlayerInput(self):
      left = pygame.key.get_pressed()[pygame.K_a]
      right = pygame.key.get_pressed()[pygame.K_d]
      jump = pygame.key.get_pressed()[pygame.K_SPACE]

      return (left, right, jump)

   def jump(self):
      self.jumping = True
      self.velocity.y = self.velocity.y - 5

   def update(self, delta):

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


#Pothole simple red rectangle for now
class Pothole():
   def __init__(self, screen, x, y, vx, vy):
      pygame.draw.rect(screen, (255,0,0), (x,y, x+442,y+40), 0)
      self.position = vector2(x, y)
      self.velocity = vector2(vx, vy)
      self.accel = .1

   def update(self, delta):
     self.position.y = delta %768

   def draw(self, screen):
      #pygame.draw.rect(screen, (255,5,0), (self.position.x,self.position.y, self.position.x+442,self.position.y-200), 0)
      pygame.draw.rect(screen, (255,5,0), (self.position.x,self.position.y, self.position.x + 442, 80), 0)

   def checkCollision(self, list, screen):
      return True




