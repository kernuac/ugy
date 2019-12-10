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

    def update(self, scr):
        for e in pygame.event.get([QUIT, KEYDOWN]):
            if e.type == QUIT:
                sys.exit(-1)
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.state = MENU
        self.mundo.update(scr)    
