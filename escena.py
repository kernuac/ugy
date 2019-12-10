import pygame
import mapa
import objeto
import personaje
import evento
import window
from xml.dom.minidom import parse
import aplicacion
from pygame.locals import KEYDOWN, K_UP, K_RIGHT, K_LEFT, K_DOWN
## Constantes  
NORTE = "N"
SUR = "S"
ESTE = "E"
OESTE = "O"

class Escena:
    xdoc = None
    mapa = None
    personajes = None
    scrollx = None
    scrolly = None
    
    def __init__(self, xdoc):
        
        """Inicializamos la escena Creando los objetos pertinentes a
        partir de un archivo xml. Este archivo Contiene los datos de 
        inicio del mapa, objetos, y personajes de la presente escena"""
        
        self.xdoc = parse(xdoc)
        self.mapa = mapa.Mapa(self.xdoc)
        self.scrollx = 0
        self.scrolly = 0
        self.eventos = self.load_events()
    
    def mover_scroll(self, x, y):
        """Movemos el scroll, esto simula el efecto "Camara" """
        self.scrollx += x
        self.scrolly += y

    
    def update(self, wd):
        """Actualiza el mapa y los personajes"""
        self.eventos[0].update(wd)
        self.eventos[1].update(wd)
        

    def get_tile(self, capa, x, y):
        return capa[x][y]
        
    def scroll_limite_izq(self):
        if self.scrollx <= 0:
            self.scrollx = 0
            op = True
        else:
            op = False
        return op
        
    def scroll_limite_der(self):
        if self.scrollx + window.TAMX >= self.mapa.tamx * 16:
            self.scrollx = self.mapa.tamx * 16 - window.TAMX
            op = True
        else:
            op = False
        return op
        
    def scroll_limite_sup(self):
        if self.scrolly <= 0:
            self.scrolly = 0
            op = True
        else:
            op = False
        return op
        
    def scroll_limite_inf(self):
        if self.scrolly + window.TAMY >= self.mapa.tamy * 16:
            self.scrolly = self.mapa.tamy * 16 - window.TAMY
            op = True
        else:
            op = False
        return op
        
    def add_characters(self, *personajes):
        #for per in personajes
        pass
    
    def create_event(self, evnt):
        e = None
        atr = evnt.attributes.get
        if atr("type").value == "teleport":
            e = evento.Teleport(atr("name").value, int(atr("x").value),
                             int(atr("y").value), int(atr("dx").value),
                             int(atr("dy").value), atr("map").value, 
                            int(atr("psx").value), int(atr("psy").value),
                             int(atr("sx").value), int(atr("sy").value),
                             atr("required").value)
        elif atr("type").value == "door":
            e = evento.Door(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("ox").value), int(atr("oy").value),
                            int(atr("cx").value), int(atr("cy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "keydoor":
            e = evento.KeyDoor(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("ox").value), int(atr("oy").value),
                            int(atr("cx").value), int(atr("cy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "doorpasswd":
            e = evento.DoorPasswd(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("ox").value), int(atr("oy").value),
                            int(atr("cx").value), int(atr("cy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "buttonfloor":
            e = evento.ButtonFloor(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("ox").value), int(atr("oy").value),
                            int(atr("cx").value), int(atr("cy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "buttonfloormath":
            e = evento.ButtonFloorMath(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("ox").value), int(atr("oy").value),
                            int(atr("cx").value), int(atr("cy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "switchfloor":
            e = evento.SwitchFloor(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("drx").value), int(atr("dry").value),
                            int(atr("izx").value), int(atr("izy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "switchfloormath":
            e = evento.SwitchFloorMath(atr("name").value, int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("drx").value), int(atr("dry").value),
                            int(atr("izx").value), int(atr("izy").value),
                            int(atr("h").value), int(atr("w").value),
                            atr("required").value)
        elif atr("type").value == "block":
            e = evento.Block(atr("name").value, int(atr("x").value),
                             int(atr("y").value), int(atr("dx").value),
                             int(atr("dy").value), atr("src").value,
                             int(atr("ix").value), int(atr("iy").value),
                             int(atr("h").value), int(atr("w").value),
                             atr("required").value)
        elif atr("type").value == "keyblock":
            e = evento.KeyBlock(atr("name").value, int(atr("x").value),
                             int(atr("y").value), int(atr("dx").value),
                             int(atr("dy").value), atr("src").value,
                             int(atr("ix").value), int(atr("iy").value),
                             int(atr("h").value), int(atr("w").value),
                             atr("required").value)
        elif atr("type").value == "chest":
            e = evento.Chest(atr("name").value, int(atr("x").value),
                             int(atr("y").value), int(atr("dx").value),
                             int(atr("dy").value), atr("src").value,
                             int(atr("ox").value), int(atr("oy").value),
                             int(atr("cx").value), int(atr("cy").value),
                             int(atr("h").value), int(atr("w").value),
                             atr("required").value, atr("item").value)
        elif atr("type").value == "chestpasswd":
            e = evento.ChestPasswd(atr("name").value, int(atr("x").value),
                             int(atr("y").value), int(atr("dx").value),
                             int(atr("dy").value), atr("src").value,
                             int(atr("ox").value), int(atr("oy").value),
                             int(atr("cx").value), int(atr("cy").value),
                             int(atr("h").value), int(atr("w").value),
                             atr("required").value, atr("item").value)
        return e
            
    def load_events(self):
        e = []
        tags = self.xdoc.getElementsByTagName("evento")
        nd = pygame.sprite.RenderUpdates()
        d = pygame.sprite.RenderUpdates()
        if len(tags) > 0:
            for ev in tags:
                if ev.attributes.get("type").value == "teleport":
                    nd.add(self.create_event(ev))
                else:
                    d.add(self.create_event(ev))
        e.append(nd)
        e.append(d)
        return e
