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

       if self.position.y >= self.screen.get_height() - self.image.get_width()/2:
           self.position.y = self.screen.get_height() - self.image.get_width()/2
           self.velocity.y = -self.velocity.y

       if self.position.y <= 0 + self.image.get_width()/2:
           self.position.y = 0 + self.image.get_width()/2
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
       pygame.draw.circle(screen, (255,0,0), (int(self.position.x)+self.image.get_width()/2, int(self.position.y)), self.image.get_width() / 2, 4)

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
      self.accel = 1
      self.previous = self.position
      self.radius = self.image.get_width()
      self.jumping = False

   def update(self, delta):

      #get Input
      controls = self.getPlayerInput()


      if controls[0] == 1 and controls[1] == 0 and controls[2] == 0 and self.jumping != True:
         self.position.x = self.position.x - 1
         print self.position.x

      elif controls[0] == 0 and controls[1] == 1 and controls[2] == 0 and self.jumping != True:
         self.position.x = self.position.x + 1
         print self.position.x

      elif controls[0] == 0 and controls[1] == 0 and controls[2] == 1 and self.jumping != True:
         self.jump()



      #update physics
      if self.jumping:
         #self.previous = self.position
         self.position = self.position.add(self.velocity.scale((pygame.time.get_ticks()* .25) - delta ))
         print self.position
         self.velocity.y = self.velocity.y + self.accel
         if self.position.y >= 768-280:
            self.velocity.y = 0
            self.jumping = False
      
         
      
      #keep in boundaries

      if self.position.y >= self.screen.get_height() - self.image.get_width()/2:
         self.position.y = self.screen.get_height() - self.image.get_width()/2
         self.velocity.y = -self.velocity.y

      if self.position.y <= 0 + self.image.get_width()/2:
         self.position.y = 0 + self.image.get_width()/2
         self.velocity.y = -self.velocity.y

      if self.position.x >= self.screen.get_width() - self.image.get_width():
         self.position.x = self.screen.get_width() - self.image.get_width()
         self.velocity.x = -self.velocity.x

      if self.position.x <= 0:
         self.position.x = 0
         self.velocity.x = -self.velocity.x

   def getPlayerInput(self):
      left = pygame.key.get_pressed()[pygame.K_a]
      right = pygame.key.get_pressed()[pygame.K_d]
      jump = pygame.key.get_pressed()[pygame.K_SPACE]

      return (left, right, jump)

   def jump(self):
      self.jumping = True
      self.velocity.y = self.velocity.y - 20
  

      
      
