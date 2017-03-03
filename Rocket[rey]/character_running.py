import pygame
import sys
import math

class vector2:
    def __init__( self, x=0, y=0 ):
        self.x = x
        self.y = y

    def xy( self ):
        return (self.x,self.y)

    def add( self, v2 ):
        result = vector2()
        result.x = self.x + v2.x
        result.y = self.y + v2.y
        return result

    def sub( self, v2 ):
        result = vector2()
        result.x = self.x - v2.x
        result.y = self.y - v2.y
        return result

    def scale( self, s ):
        result = vector2()
        result.x = self.x * s
        result.y = self.y * s
        return result

    def mag( self ):
        return math.sqrt( self.x * self.x + self.y * self.y )
   
    def normalized( self ):
        result = vector2()
        m = self.mag()
        if m == 0:
            return vector2( 0, 0 )
        result.x = self.x / m
        result.y = self.y / m
        return result

pygame.mixer.pre_init( 44100, -16, 2 )
pygame.init()
screen = pygame.display.set_mode( (600,225) )


img = pygame.image.load( "run_character.png" ).convert_alpha()
MARGIN = 200
IMG_W = 200

frame = 0
frame_timer = 0
FRAME_TIME = 90
FRAME_CT = 4

loc = vector2(120,300)
v = vector2(0,0)
SPEED = 0.2

#dp = pygame.mixer.Sound( "shoryuken.wav" )

#pygame.mixer.music.load( "theme.wav" )
#pygame.mixer.music.play()

start_time = pygame.time.get_ticks()

while True:
    pygame.event.pump()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
            #dp.play()
            frame = 1
            frame_timer = 0
            v.y = 0 #-0.3

    delta = pygame.time.get_ticks() - start_time
    start_time = pygame.time.get_ticks()

    if loc.y == 80:
        #grounded
        inputX = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            inputX -= 1
        if keys[pygame.K_d]:
            inputX += 1

        if inputX != 0:
            v.x = inputX * SPEED
        elif v.x > 0:
            v.x = v.x - 0.001 * delta
            v.x = 0
        elif v.x < 0:
            v.x = v.x + 0.001 * delta
            if v.x > 0:
                v.x = 0
            
    else:
        # in the air
        v.y = v.y + 0.001 * delta

    loc = loc.add( v.scale( delta ) )

    if loc.y > 65:
        loc.y = 65
        v.y = 0

    clip = pygame.Rect( MARGIN+IMG_W*frame, 0, IMG_W, 160 )

    #if frame > -1:
    #    if frame_timer > FRAME_TIME:
    #        frame_timer -= FRAME_TIME
    #        frame = (frame+1) % FRAME_CT
    #        print "Frame:" , frame
    #    frame_timer += delta

    print "frame:" , frame
    if frame >= 0:
        if frame_timer > FRAME_TIME:
            frame_timer -= FRAME_TIME
            frame = (frame+1) % FRAME_CT
        frame_timer += delta
        
    screen.fill( (255, 255, 255) )

    
    #screen.blit( stage, (0,0) )
    screen.blit( img, loc.xy(), area=clip, special_flags=pygame.BLEND_RGBA_MIN )

    pygame.display.flip()

