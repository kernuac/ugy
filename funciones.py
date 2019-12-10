import pygame
import xml

def cargar_bits(xdoc, var):
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
    
def cargar_tiles(xdoc):
    i = {}
    ts = xdoc.getElementsByTagName("tileset")[0]
    img = pygame.image.load(ts.attributes.get("src").value).convert()
    t = ts.getElementsByTagName("tile")
    for d in t:
        i[d.attributes.get("tipo").value] = cargar_tile(img,
                             int(d.attributes.get("x").value),
                             int(d.attributes.get("y").value),
                             int(d.attributes.get("h").value),
                             int(d.attributes.get("w").value))
    return i
    

    
        
        
def coordMapa(x, y):
    return (x / 16, y / 16)

def esSolido(map, x, y):
    return map[y][x]

def oscurecerPantalla(scr):
    negro = pygame.Surface(scr.get_size())
    clock = pygame.time.Clock()
    for i in range(0, 255, 5):
        negro.set_alpha(i)
        scr.blit(negro,(0, 0))
        pygame.display.update()
        clock.tick(20)

def cargar_imagenes(img):
    im = []
    for i in img:
        im.append(cargar_imagen(i))
    return im
    
def cargar_imagen(img):
    return pygame.image.load(img).convert()

def cargar_imagen_at(im, x, y, tx, ty):
    nwimg = pygame.Surface((tx, ty))
    nwimg.blit(im, (0, 0), (x, y, tx, ty))
    nwimg.set_colorkey((255, 0, 255))
    return nwimg
    
def colisionan(r1, r2):
    op = False
    if r1.colliderect(r2):
        op = True
    return op
    
def cargar_atributos(xdoc, tag, attrb):
    tags = xdoc
    return tag.attributes.get(attrb).value
