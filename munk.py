import pygame
import pymunk
import random

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_UP,
    K_DOWN,
    KEYDOWN,
    KEYUP,
    QUIT,
)

from pymunk.pygame_util import DrawOptions

FPS	    = 60

clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0,0.0001

class Player():

    def __init__(self,x,y,r):
        self.r = r
        self.body = pymunk.Body()
        self.body.mass = 0.1
        self.body.position = x,y
        self.shape = pymunk.Poly.create_box(self.body,(self.r,self.r))
#        self.shape = pymunk.Circle(self.body,self.r)
        self.shape.friction = 0.5
        self.shape.density = 0.1
        self.shape.elasticity = 0.9
        space.add(self.body,self.shape)
        self.color = (0,250,0)


class Platform():
    def __init__(self, x, y, l, h):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x,y)
        self.shape = pymunk.Poly.create_box(self.body, (l, h))
        self.shape.friction = 0.5
        self.shape.elasticity = 0.8
        space.add(self.body,self.shape)
        self.color = (100,100,100)

class Text():
    def __init__(self):
        self.font = pygame.font.SysFont('Consolas', 30)
    
    def set_text(self,str):
        self.surface = self.font.render(str, False, (200,0,0), 0)

    def draw(self,screen):
        screen.blit(self.surface,(0,0))
        

def main():

    pygame.init()
    pygame.font.init() 

    flags = pygame.DOUBLEBUF & pygame.HWSURFACE
    resolution = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode(resolution,flags, vsync=1)

    DRAW_OPTIONS = DrawOptions(screen)

    running = True

    player = Player(1440/2,800/2,30)

    ground = Platform(1440/2,800,1440,100)
    roof = Platform(1440/2,0,1440,100)
    left_wall = Platform(0,400,100,800)
    right_wall = Platform(1440,400,100,800)

    gtxt = Text()

    while running:

        screen.fill((0,0,0))
 
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    player.body.velocity = (0.1,0)
                if event.key == K_LEFT:
                    player.body.velocity = (-0.1,0)
                if event.key == K_UP:
                    player.body.velocity = (0,1)

            if event.type == KEYUP:
                player.body.velocity = (0,0)


            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False


        gtxt.set_text(f"Ball")
        gtxt.draw(screen)

        space.debug_draw(DRAW_OPTIONS)

        pygame.display.flip()
        space.step(FPS/1)

    pygame.quit()

if __name__ == "__main__":
    main()

