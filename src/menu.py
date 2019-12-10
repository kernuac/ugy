import pygame
import sys
import time
import juego
import funciones
from pygame.locals import K_UP, K_DOWN, K_RETURN, QUIT, KEYDOWN

## constantes
# Estados
WAIT = 0
PLAY = 1
EXIT = 2

class Menu:
    acciones = None
    background = None
    accion = None
    font = None
    transicion = None
    alpha = None
    state = None
    def __init__(self):
        """inicializamos las variables importantes para el Menu"""
        self.acciones = {0:'comenzar', 1:'salir'}
        self.background = None
        self.accion = 0
        self.font = pygame.font.Font(None, 26)
        self.transicion = 1
        self.alpha = 255
        self.state = WAIT
        
    def get_state(self):
        return self.state
    
    def update(self, scr):
        """Actualizamos el cursor seleccionador de opciones en el Menu"""
        
        for e in pygame.event.get([QUIT, KEYDOWN]):
            if e.type == QUIT:
                sys.exit(-1)
            elif e.type == KEYDOWN:
                if e.key == K_UP and self.accion > 0:
                    self.accion -= 1
                elif (e.key == K_DOWN and 
                      self.accion < len(self.acciones) - 1):
                    self.accion += 1
                elif e.key == K_RETURN:
                    if self.accion == 0:
                        self.state = PLAY
                        pygame.event.clear()
                    elif self.accion == 1:
                        self.state = EXIT
        self.show(scr)

    def show(self, scr):
        """Imprimimos el menu en pantalla, con una pequenia transicion. 
        Esto se logra imprimiendo, sobre la imagen del menu, una 
        superficie negra. Esta ultima se ira atenuando hasta ser 
        totalmente invisible (set_alpha)"""
        
        scr.fill((0, 0, 0))
        negro = pygame.Surface(scr.get_size())
        negro.fill((0, 0, 0))
        negro.set_alpha(self.alpha)
        text = []
        if self.background != None:
            scr.blit(self.background, (0, 0))
            
        for i in range(len(self.acciones)):
            if self.accion == i:
                text.append(self.font.render("> " + self.acciones[i],
                                                  True, (255, 255, 0)))
            else:
                text.append(self.font.render(self.acciones[i],
                                         True, (255, 255, 255)))
                
            scr.blit(text[i], (scr.get_size()[0] / 2,
                     i * 20 + scr.get_size()[1] / 2))
        
        if self.transicion == 1 and self.alpha > 0:
            self.alpha -= 10
            
        if self.alpha == 0:
            self.transicion = 0
            
        scr.blit(negro, (0, 0))
        
