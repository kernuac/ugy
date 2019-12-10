import pygame
import escena 
import personaje
import system
import music
from evento import CLOSED, IZQUIERDA, DERECHA
import os
import tileset
import window
#constantes necesarias
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
JOIN = os.path.join
PATH = os.path.abspath(os.path.dirname(__file__))
DATA = JOIN(PATH, "data")

class Mundo:
    
    hero = None
    stages = None
    crrnt = None
    font = None
        
    def __init__(self):
        self.hero = personaje.Heroe("Ker", JOIN(DATA,"Heroes.png"), 0, 0, 5,
                                                     12, personaje.SUR)
        self.stages = self.load_stages()
        self.crrnt = "town"
        self.get_stage().mapa.create_map()
        self.font = pygame.font.Font(None, 20)
        self.action =  system.Action()
        self.keys = system.Key()
        music.MUSIC.play(-1)  
        
    def get_stage(self):
        return self.stages[self.crrnt]
        
    def load_stages(self):
        m = { "town":escena.Escena(JOIN(PATH, "town.xml")),
              "foresta":escena.Escena(JOIN(PATH,"foresta.xml")),
              "forestb":escena.Escena(JOIN(PATH,"forestb.xml")),
              "castlep1e":escena.Escena(JOIN(PATH,"castlep1e.xml")),
              "castlep1a":escena.Escena(JOIN(PATH,"castlep1a.xml")),
              "castlep1b":escena.Escena(JOIN(PATH,"castlep1b.xml")),
              "castlep1c":escena.Escena(JOIN(PATH,"castlep1c.xml")),
              "castlep2a":escena.Escena(JOIN(PATH,"castlep2a.xml")),
              "castlep2b":escena.Escena(JOIN(PATH,"castlep2b.xml")),
              "castlep2c":escena.Escena(JOIN(PATH,"castlep2c.xml")),
              "castlep3a":escena.Escena(JOIN(PATH,"castlep3a.xml")),
              "castlep3b":escena.Escena(JOIN(PATH,"castlep3b.xml")),
              "castlep3c":escena.Escena(JOIN(PATH,"castlep3c.xml")),
              "castlep4a":escena.Escena(JOIN(PATH,"castlep4a.xml")),
              "castlep4b":escena.Escena(JOIN(PATH,"castlep4b.xml")),
              "castlep4c":escena.Escena(JOIN(PATH,"castlep4c.xml")),
              "castlep5a":escena.Escena(JOIN(PATH,"castlep5a.xml")),
              "castlep5b":escena.Escena(JOIN(PATH,"castlep5b.xml")),
              "castlep5c":escena.Escena(JOIN(PATH,"castlep5c.xml"))
            }
        return m
        
         
    def update(self):
        self.get_stage().update(self)
        self.hero.update(self.get_stage())
        self.show()       
        ob = self.hero.collide(self.get_stage().eventos[1], self.get_stage())
        
        if ob != None:
            if(ob.type == "door" or ob.type == "doorkey"
            and ob.get_state() == CLOSED):
                self.action.set_action("Abrir")
            elif(ob.type == "chest" and ob.visible and
            ob.get_state() == CLOSED):
                self.action.set_action("Abrir")
            elif(ob.type == "keyblock" and ob.visible and
            ob.get_state() == CLOSED):
                self.action.set_action("Abrir")
            elif ob.type == "switchfloor" or ob.type == "switchfloormath": 
                if ob.get_state() == IZQUIERDA:
                    self.action.set_action("Mover ->")
                else:
                    self.action.set_action("Mover <-")
            else:
                self.action.set_action("")
        else:
            self.action.set_action("")
            if not self.hero.has_item("key"):
                self.keys.set_cnt_keys(0)
            else:
                self.keys.set_cnt_keys(self.hero.items["key"])
                
    def show(self):
        window.scr.fill((0,0,0))
        esc = self.get_stage()
        esc.mapa.show(esc.scrollx, esc.scrolly)
        for e in esc.eventos[1]:
            e.draw(esc.scrollx, esc.scrolly)
        self.hero.show()
        self.action.show(285, 5)
        self.keys.show(340,280)

    def change_stage(self, esc, sx, sy):
        last = self.crrnt
        self.get_stage().mapa.delete_map()
        self.crrnt = esc
        crrnt = self.get_stage()
        crrnt.mapa.create_map()   
        crrnt.scrollx = sx
        crrnt.scrolly = sy
        
        #print last, sx, sy
        if last == "town" and self.crrnt == "foresta":
            print "estamos"
            music.change_music("TMCMinishWoods.mid")
            music.MUSIC.play(-1)
        elif last == "forestb" and self.crrnt == "castlep1e":
            music.change_music("BlackFang.mid")
            music.MUSIC.play(-1)
        elif last == "castlep1e" and self.crrnt == "forestb":
            music.change_music("TMCMinishWoods.mid")
            music.MUSIC.play(-1)
        elif last == "foresta" and self.crrnt == "town":
            music.change_music("MinishVillageXGv1-2.mid")
            music.MUSIC.play(-1)
    
    def print_t(self, scr, text, x, y,fg=False,bg=False):
        t = self.font.render(text,True,fg,bg)
        scr.blit(t, (x * 16, y * 16))
      
