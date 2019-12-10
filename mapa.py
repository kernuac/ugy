import tileset
import funciones
import pygame
import window
from xml.dom.minidom import parse

class Mapa:
    bkgr = None
    cap1 = None 
    cap2 = None
    solid = None
    tamx = None
    tamy = None
    tileset = None
    image = None
    
    def __init__(self, xdoc):
        
        self.bkgr = self.cargar_bits(xdoc, "background")
        self.cap1 = self.cargar_bits(xdoc, "capa1")
        self.cap2 = self.cargar_bits(xdoc, "capa2")
        self.solid = self.cargar_bits(xdoc, "solidos")
        self.tamx = len(self.bkgr[0])
        self.tamy = len(self.bkgr)
        
        self.tileset = tileset.TileSet(xdoc)
        #self.image = None 
        
    def show(self, sx, sy):
        window.scr.blit(self.image, (-sx, -sy))
    
    def is_solid(self, x, y):
        return self.solid[y][x]
                
    def create_map(self):
        img = pygame.Surface((self.tamx * 16, self.tamy * 16))
        bkg = self.create_layer(self.bkgr)
        cp1 = self.create_layer(self.cap1)
        cp2 = self.create_layer(self.cap2)
        img.blit(bkg, (0, 0))
        img.blit(cp1, (0, 0))
        img.blit(cp2, (0, 0))
        self.image = img
        
    
    def delete_map(self):
        self.image = None
    
    def create_layer(self, layer):
        img = pygame.Surface((self.tamx * 16, self.tamy * 16)).convert()
        img.fill((255,0,255))
        img.set_colorkey((255,0,255))
        
        tiles = self.tileset.tiles
        
        for y in range(self.tamy):
            for x in range(self.tamx):
                if layer[y][x] != "-":
                    img.blit(tiles[layer[y][x]], (x * 16, y * 16))
        return img
        
    def cargar_bits(self, xdoc, var):
        d = []
        bits = (xdoc.getElementsByTagName(var)[0].
        getElementsByTagName("bits"))
        
        for datos in bits:
            linea = []
            for c in datos.childNodes[0].data:
                if var == "solidos":
                    linea.append(int(c))
                else:
                    linea.append(c)
            d.append(linea)
        return d
#def main():
#    pygame.init()
#    scr = pygame.display.set_mode((400, 300))
#    map = Mapa(parse("town.xml"))
#    while True:
#        map.imprimir(scr, map.bkgr)
#        map.imprimir(scr, map.cap1)
#        map.imprimir(scr, map.cap2)
#        pygame.display.update()
#        
#if __name__=="__main__": main()
