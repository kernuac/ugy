import pygame
import funciones
import time
import window
from pygame.locals import FULLSCREEN
#Constantes
RUNNING = 0
FINISHED = 1
class Intro:
    imagenes = None
    state = None
    def __init__(self, *img):
        """ definimos la introduccion del juego. El atributo (*img) corresponde a
        la imagen o conjunto de imagenes que se mostraran en el inicio del juego"""
        self.imagenes = funciones.cargar_imagenes(img)  
        self.state = RUNNING
                                                                           
    def get_state(self):
        return self.state

    def show(self):
        """mostramos la introduccion en pantalla"""
        b = pygame.Surface((480, 320))
        b.fill((0, 0, 0))
        b.set_alpha(255)
        clock = pygame.time.Clock()
        for img in self.imagenes:
            for i in range(0, 255, 5):
                b.set_alpha(255 - i)
                window.scr.blit(img,(0,0))
                window.scr.blit(b, (0, 0))
                pygame.display.update()
                clock.tick(20)
            time.sleep(3)
            for i in range(0, 255, 5):
                b.set_alpha(i)
                window.scr.blit(img, (0, 0))
                window.scr.blit(b, (0, 0))
                pygame.display.update()
                clock.tick(20)

            time.sleep(1)
        self.state = FINISHED
        pygame.event.clear()
##Esta funcion es solo para probar el modulo, descomentarla
##en caso de que quisiera probar.
#def main():
#   pygame.init()
#   scr = pygame.display.set_mode((480,320))
#   introd = Intro("data/desarrollado.png","data/derechos.png")
#   introd.mostrar(scr)

#if __name__=="__main__": main()
