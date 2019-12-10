import funciones
from xml.dom.minidom import parse
import pygame

def load_tileset(xdoc):
    i = {}
        
    ts = xdoc.getElementsByTagName("tileset")[0]
    img = load_image(ts.attributes.get("src").value).convert()
    tl = ts.getElementsByTagName("tile")
        
    for t in tl:
        atr = t.attributes.get
        i[atr("tipo").value] = load_tile(img, int(atr("x").value), 
        int(atr("y").value), int(atr("h").value), int(atr("w").value))
    return i
    
def load_tile(image, x, y, h, w):
    i = pygame.Surface((h, w)).convert()
    i.blit(image, (0, 0), (x, y, h, w))
    i.set_colorkey((255, 0, 255))
    return i

def load_image(img):
    return pygame.image.load(img)
    
class TileSet:
    tiles = None
    def __init__(self, xdoc):
        self.load_tile = load_tile
        self.load_tileset = load_tileset
        self.load_image = load_image
        self.tiles = self.load_tileset(xdoc)


#def main():
#   pygame.init()
#   scr = pygame.display.set_mode((400,300))
#   ts = TileSet(parse("town.xml"))
#   while True:
#       scr.blit(ts.tiles["."],(0,0))
#       pygame.display.update()
        
#if __name__=="__main__": main()

