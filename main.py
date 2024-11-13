import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class Player():
    def __init__(self,x,y,r):
        self.name = "Player"
        self.grounded = False
        self.color = (0,250,0)
        (self.x,self.y,self.r) = (x,y,r)
        (self.dx,self.dy) = (0,0)

    def tick(self):
        if self.dy > 0:
            self.y += self.dy
        if self.grounded:
            self.x += self.dx
            self.dy = 0
            if self.dx > 0:
                self.dx -= 0.01
            if self.dx < 0:
                self.dx += 0.01
        else:
                self.dy -= 0.01
                self.y -= self.dy

    def move(self,x = 0,y = 0):
        self.dx = x

    def bounce(self):
        self.dy = 1

    def check_grounded(self,platforms):
        for platform in platforms:
            if self.x+self.r/2 >= platform.x and self.x-self.r/2 <= (platform.x+platform.l):
                if self.y+self.r > platform.y and self.y+self.r <= platform.y+platform.h:
                    self.grounded = True
                    return True
        self.grounded = False
        return False

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y), 15)

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

    player = Player(x,y-20,15)

    gtxt = Text()

    platforms = []
    platforms.append(Platform(x-80, y+20, 300))

    platforms.append(Platform(20, 40, 300))
    platforms.append(Platform(200, 80, 300))
    platforms.append(Platform(190, 160, 300))
    platforms.append(Platform(700, 240, 300))
    platforms.append(Platform(1200, 320, 300))
    platforms.append(Platform(400, 480, 300))
    platforms.append(Platform(500, 580, 300))
    platforms.append(Platform(1500, 640, 300))

    while running:

        screen.fill((0,0,0))

        gtxt.set_text("Grounded: "+str(player.check_grounded(platforms))+ " dx: "+str(player.dx)+" dy: "+str(player.dy))
        gtxt.draw(screen)
 

 

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player.grounded:
            player.move(x = -1)
        if keys[K_RIGHT] and player.grounded:
            player.move(x = 1)
        if keys[K_SPACE] and player.grounded:
            player.bounce()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        player.tick()

        player.draw(screen)
        for platform in platforms:
#            platform.move(y = 0.11)
            platform.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
