import pygame
import random
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_UP,
    K_DOWN,
    KEYDOWN,
    QUIT,
)

SPEED       = 0.8
SIZE        = 25
FRICTION    = 0.01
GRAVITY     = 0.01
BOUNCE      = 2

class Player():

    def __init__(self,x,y,r):
        self.grounded = False
        self.color = (0,250,0)
        (self.x,self.y,self.r) = (x,y,r)
        (self.dx,self.dy) = (0,0)

    def tick(self):
        self.x += self.dx
        self.y += self.dy
        if abs(self.dx) < 0.1:
            self.dx = 0
        if self.grounded:
            self.dy = 0
            if self.dx > 0:
                self.dx -= FRICTION
            if self.dx < 0:
                self.dx += FRICTION
        else:
                self.dy += GRAVITY

    def move(self,x = 0,y = 0):
        self.dx = x
        self.dy = y

    def bounce(self):
        self.dy = -BOUNCE
        self.y += self.dy

    def drop(self):
        self.dy = 1
        self.y += self.dy

    def check_grounded(self,platforms):
        for platform in platforms:
            if self.x >= platform.x and self.x <= (platform.x+platform.l): # above platform
                if abs(round(self.y+self.r) - round(platform.y)) <= 3 * (GRAVITY*100): # on platform
                    self.grounded = True
                    return True
        self.grounded = False
        return False

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y), self.r, 1)


class Platform():
    def __init__(self, x, y, l):
        (self.x,self.y, self.l, self.h) = (x,y,l,10)
        self.color = (100,100,100)
        self.rect = pygame.Rect(x,y,self.l, self.h)
    
    def move(self,x = 0,y = 0):
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x,self.y,self.l, self.h)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


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

    #flags = pygame.FULLSCREEN
    screen = pygame.display.set_mode(([1920, 1280]),flags = 0, vsync=1)
    running = True
    x =  1920/2; y = 1280 / 2

    player = Player(x,y-100,SIZE)

    gtxt = Text()

    platforms = []
#    platforms.append(Platform(x-80, y+15, 300))

    for _ in range(20): # create platforms at random placements
        platforms.append(Platform(random.randint(1,1920-100), random.randint(1,1280-100), random.randint(100,400)))


    while running:

        screen.fill((0,0,0))
 
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player.grounded:
            player.move(x = -SPEED)
        if keys[K_RIGHT] and player.grounded:
            player.move(x = SPEED)
        if (keys[K_SPACE] or keys[K_UP]) and player.grounded:
            player.bounce()
        if keys[K_DOWN] and player.grounded:
            player.drop()

        player.check_grounded(platforms)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        player.tick()

        gtxt.set_text(f"dx: {player.dx: .2f} dy: {player.dy: .2f} Speed: {SPEED} Friction: {FRICTION} Gravity: {GRAVITY}")
        gtxt.draw(screen)

        player.draw(screen)
        for platform in platforms:
#            platform.move(y = 0.01)
            platform.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
