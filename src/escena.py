import pygame
import mapa
import objeto
import personaje
import evento
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
        #self.objetos = None
        #self.personajes = personaje.Personaje("cristhian",
        #"data/Heroes.png",3,0,10,10,personaje.OESTE,"hola soy un personaje")
        self.scrollx = 0
        self.scrolly = 0
        self.eventos = self.load_events()
        #self.limites = None
    
    def mover_scroll(self, x, y):
        """Movemos el scroll, esto simula el efecto "Camara" """
        self.scrollx += x
        self.scrolly += y

    
    def update(self, wd):
        """Actualiza el mapa y los personajes"""
        self.eventos[0].update(wd)
        self.eventos[1].update(wd)
        #Solo para debugging
        #
        #self.personajes.actualizar(self)
        

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
        if self.scrollx + aplicacion.TAMX >= self.mapa.tamx * 16:
            self.scrollx = self.mapa.tamx * 16 - aplicacion.TAMX
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
        if self.scrolly + aplicacion.TAMY >= self.mapa.tamy * 16:
            self.scrolly = self.mapa.tamy * 16 - aplicacion.TAMY
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
                             int(atr("sx").value), int(atr("sy").value))
        elif atr("type").value == "door":
            e = evento.Door(int(atr("x").value),
                            int(atr("y").value), int(atr("dx").value),
                            int(atr("dy").value), atr("src").value,
                            int(atr("ox").value), int(atr("oy").value),
                            int(atr("cx").value), int(atr("cy").value),
                            int(atr("h").value), int(atr("w").value))
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
                elif ev.attributes.get("type").value == "door":
                    d.add(self.create_event(ev))
        e.append(nd)
        e.append(d)
        return e
