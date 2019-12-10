import pygame
import escena 
import personaje
import system
from evento import CLOSED
#constantes necesarias
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)

class Mundo:
    
    hero = None
    stages = None
    crrnt = None
    font = None
        
    def __init__(self):
        self.hero = personaje.Heroe("Ker", "data/Heroes.png", 0, 0, 5,
                                                     10, personaje.SUR)
        self.stages = self.load_stages()
        self.crrnt = "castlep1e"
        self.get_stage().mapa.create_map()
        self.font = pygame.font.Font(None, 20)
        pygame.mixer.music.load("data/MinishVillageXGv1-2.mid")
        pygame.mixer.music.play(-1)
        self.action =  system.Action()  
    def get_stage(self):
        return self.stages[self.crrnt]
        
    def load_stages(self):
        m = { "town":escena.Escena("town.xml"),
              "foresta":escena.Escena("foresta.xml"),
              "castlep1e":escena.Escena("castlep1e.xml"),
              "castlep1a":escena.Escena("castlep1a.xml"),
              "castlep1b":escena.Escena("castlep1b.xml"),
              "castlep1c":escena.Escena("castlep1c.xml"),
              "castlep2a":escena.Escena("castlep2a.xml"),
              "castlep2b":escena.Escena("castlep2b.xml"),
              "castlep2c":escena.Escena("castlep2c.xml"),
              "castlep3a":escena.Escena("castlep3a.xml"),
              "castlep3b":escena.Escena("castlep3b.xml"),
              "castlep3c":escena.Escena("castlep3c.xml"),
              "castlep4a":escena.Escena("castlep4a.xml"),
              "castlep4b":escena.Escena("castlep4b.xml"),
              "castlep4c":escena.Escena("castlep4c.xml"),
              "castlep5a":escena.Escena("castlep5a.xml"),
              "castlep5b":escena.Escena("castlep5b.xml"),
              "castlep5c":escena.Escena("castlep5c.xml")
            }
        return m
        
         
    def update(self, scr):
        #self.EscActual().personajes.actualizar()
        self.get_stage().update(self)
        self.hero.update(self.get_stage(), scr)
        self.show(scr)       
        ob = self.hero.collide(self.get_stage().eventos[1], self.get_stage())
        if ob != None:
            if ob.type == "door" and ob.get_state() == CLOSED:
                self.action.set_action("Abrir")
            else:
                self.action.set_action("")
        else:
            self.action.set_action("")
    def show(self, scr):
        esc = self.get_stage()
        esc.mapa.show(scr, esc.scrollx, esc.scrolly)
        for e in esc.eventos[1]:
            e.draw(scr, esc.scrollx, esc.scrolly)
        self.hero.show(scr)
        self.action.show(scr, 285, 5)
        self.print_t(scr,"hero: %s" %(self.hero.name),0,0,WHITE,BLACK)
        self.print_t(scr,"sx: %i sy: %i" %(esc.scrollx, esc.scrolly),0,1,WHITE,BLACK)
        self.print_t(scr,"room: %s" %(self.crrnt),0,2,WHITE,BLACK)
    
    def change_stage(self, esc, sx, sy):
        self.get_stage().mapa.delete_map()
        self.crrnt = esc
        self.get_stage().mapa.create_map()   
        self.get_stage().scrollx = sx
        self.get_stage().scrolly = sy
    
    def print_t(self, scr, text, x, y,fg=False,bg=False):
        t = self.font.render(text,True,fg,bg)
        scr.blit(t, (x * 16, y * 16))
