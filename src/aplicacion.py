import pygame
import intro
import menu
import sys
import juego
from pygame.locals import FULLSCREEN

# Constantes
INTRO = 0
MENU = 1
GAME = 2
EXIT = 3
TAMX = 400
TAMY = 300

class Aplicacion:
    
    scr = None
    state = None
    intro = None
    menu = None
    juego = None
    
    def __init__(self, op):
        """Inicializamos las variables necesarias para la aplicacion.
        Creamos la pantalla, definimos los estados y creamos los objetos
        pertinentes."""
        self.scr = pygame.display.set_mode((TAMX, TAMY))
        self.state = INTRO
        self.intro = intro.Intro("data/desarrollado.png",
                                     "data/derechos.png") 
        self.menu = menu.Menu()
        self.juego = juego.Juego()
    
    def get_state(self):
        """Retorna el estado actual de la Aplicacion"""
        return self.state

    def loop( self ):
        """el loop principal, se ejecutara constantemente hasta que en
        algun lugar se seleccione Salir"""
        clock = pygame.time.Clock()
        while self.get_state() is not EXIT:
            self.update()
            pygame.display.update()
            clock.tick(20)
            
    def update(self):
        """ Ejecuta una accion dependiendo del estado actual del juego,
        intro, indica que el juego esta mostrando la introduccion. Cuan-
        do esta termine, pasara al estado Menu. Este estado mostrara el
        Menu Principal y estara la espera de la seleccion de alguna 
        opcion (por ahora, jugar y salir). Si selecciona Jugar, cargara
        las variables necesarias para ejecutar el juego. Si selecciona 
        Salir, se termina la aplicacion."""
        
        if self.get_state() is INTRO:
            if self.intro.get_state() is intro.RUNNING:
                self.intro.show(self.scr)
                
            elif self.intro.get_state() is intro.FINISHED:
                self.state = MENU
                
        elif self.get_state() is MENU:
            if self.menu.get_state() is menu.WAIT:
                self.menu.update(self.scr)
                
            elif self.menu.get_state() is menu.EXIT:
                pygame.quit()
                print "byee!"
                sys.exit(-1)
                
            elif self.menu.get_state() is menu.PLAY:
                self.state = GAME
                self.juego.state = juego.RUN
                
        elif self.get_state() is GAME:
            if self.juego.get_state() is juego.RUN:
                self.juego.update(self.scr)

            elif self.juego.get_state() is juego.MENU:
                self.state = MENU
                self.menu.state = menu.WAIT
