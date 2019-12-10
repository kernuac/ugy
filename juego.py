import pygame
from pygame.locals import K_ESCAPE,QUIT,KEYDOWN
import mundo
#Constantes
RUN = 0
MENU = 1

class Juego:
    state = None
    mundo = None
    def __init__(self):
        self.state = 0
        self.mundo = mundo.Mundo()

    def get_state(self):
        return self.state

    def update(self):
        for e in pygame.event.get([QUIT, KEYDOWN]):
            if e.type == QUIT:
                sys.exit(-1)
            t = pygame.key.get_pressed()
            if t[K_ESCAPE]:
                    self.state = MENU
        self.mundo.update()    
