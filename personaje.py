import pygame
import funciones
import aplicacion
import tileset
import time
import system
import window
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, KEYDOWN, K_ESCAPE, KEYDOWN, KEYUP, K_F11
from tileset import load_tile, load_image

#constantes necesarias
NORTE = 0
SUR = 1
ESTE = 2
OESTE = 3

class Personajes:
    
    name = None
    images = None
    dir = None
    crrnt_frame = None
    rect = None
    feet = None
    items = None
    delay = None
    cnt = None
    lastx = None
    lasty = None
    def __init__(self, nom, spr, x, y, psx, psy, dir):
        self.name = nom
        self.images = self.load_sprites(spr, x, y)
        self.dir = dir
        self.crrnt_frame = 1
        self.rect = self.images[self.dir][self.crrnt_frame].get_rect()
        self.feet = pygame.Rect((self.rect.x + 8, self.rect.y + 16, 16, 16))
        self.items = {}
        self.delay = 2 
        self.cnt = 0
        self.move(psx * 16, psy * 16)

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.feet.move_ip(x, y)
        self.lastx = x
        self.lasty = y

    def update(self, esc):
        pass
        
    def show(self):
        window.scr.blit(self.images[self.dir][self.crrnt_frame], self.rect)
        
    def load_sprites(self, spr, x, y):
        img = pygame.Surface((32, 32))
        im = load_image(spr).convert()
        img.set_colorkey((255, 0, 255))
        
        a = []
        b = []
        e = []
        d = []
        c = 0
        
        for j in range(0, 4):
            if j > 2:
                c -= 2   
                       
            a.append(load_tile(im, x * 32 + c * 32, y * 32, 32, 32))
            b.append(load_tile(im, x * 32 + c * 32, y * 32 + 32, 32, 32))
            e.append(load_tile(im, x * 32 + c * 32, y * 32 + 64, 32, 32))
            d.append(load_tile(im, x * 32 + c * 32, y * 32 + 96, 32, 32))
            
            c += 1
            
        return { SUR:a, OESTE:b, ESTE:e, NORTE:d }   

    def get_item( self, item ):
        if not self.has_item( item ):
            self.items[ item ] = 0
        self.items[ item ] += 1
         
    def has_item( self, item ):
        return self.items.has_key( item )
                
    def change_dir( self, dir ):
        self.dir = dir
        
    def del_item( self, item ):
        if self.has_item( item ):
            self.items[ item ] -= 1
        if self.items[ item ] == 0:
            del self.items[ item ]
    
    def animar( self ):
        self.caminar = 1
        if self.cnt < 0:
            self.crrnt_frame += 1
            self.cnt = self.delay
        else:
            self.cnt -= 1
        if self.crrnt_frame >= 4:
            self.crrnt_frame = 0
    
    def w_coord(self, x, y, esc):
        x = x / 16
        y = y / 16
        return [x, y]
    
    def can_walk(self, x, y, esc):
        op = True
        dx, dy = self.w_coord(x, y, esc)
        if esc.mapa.is_solid(dx, dy):
            op = False
        return op
        
        
class Personaje(Personajes):
    def __init__(self, nom, spr, x, y, psx, psy, dir, texto,
                          accion=None, ruta=None, item=None):
        Personajes.__init__(self, nom, spr, x, y, psx, psy, dir)
        self.ruta = ruta
        self.texto = texto
    
    def update(self, esc):
        pass

        
    def show(self, sx, sy):
        img = self.images[self.dir][self.crrnt_frame]
        window.scr.blit(img, (self.rect.x - sx, self.rect.y - sy))
        
    def action(self):
        while not pygame.key.get_pressed() == [K_RETURN]:
            print texto
        
class Heroe(Personajes):
    def __init__(self, nom, spr, x, y, psx, psy, dir):
        Personajes.__init__(self, nom, spr, x, y, psx, psy, dir)
    
    def update(self, esc):
        #obj = self.collide(esc.personajes, esc)
        obj = self.collide(esc.eventos[1], esc)
        t = pygame.key.get_pressed()

        if t[K_DOWN]:
            if self.can_walk(self.feet.centerx + esc.scrollx,
            self.feet.bottom + esc.scrolly, esc):
                self.change_dir(SUR)
                self.animar()
                if (not esc.scroll_limite_inf() and 
                self.feet.centery > window.TAMY / 2):
                    esc.mover_scroll(0, 5)
                else:
                    self.move(0, 5)
                
        elif t[K_UP]:
            if self.can_walk(self.feet.centerx + esc.scrollx,
            self.feet.top + esc.scrolly, esc):
                self.change_dir(NORTE)
                self.animar()
                if (not esc.scroll_limite_sup() and
                self.feet.centery < window.TAMY / 2):
                    esc.mover_scroll(0, -5)
                else:
                    self.move(0, -5)
               
        elif t[K_LEFT]:
            if self.can_walk(self.feet.left + esc.scrollx,
            self.feet.centery + esc.scrolly, esc):
                self.animar()
                self.change_dir(OESTE)
                if (not esc.scroll_limite_izq() and
                self.feet.centerx < window.TAMX / 2):
                    esc.mover_scroll(-5, 0)
                else:
                    self.move(-5, 0)
                
        elif t[K_RIGHT]:
            if self.can_walk(self.feet.right + esc.scrollx,
            self.feet.centery + esc.scrolly, esc):
                self.change_dir(ESTE)
                self.animar()
                if (not esc.scroll_limite_der() and
                self.feet.centerx > window.TAMX / 2):
                    esc.mover_scroll(5, 0)
                else:
                    self.move(5, 0)
        elif t[K_SPACE]:
            if obj is not None:
                time.sleep(0.5)
                obj.action(esc.eventos[1])
        elif t[K_F11]:
            time.sleep(0.5)
            pygame.display.toggle_fullscreen()        
    
    def collide(self, objects, esc):
        obj = None
        if len(objects) > 0:
            for ob in iter(objects):
                if(self.rect.colliderect(pygame.Rect(ob.rect.x - 
                    esc.scrollx, ob.rect.y - esc.scrolly, 32, 32))
                  and ob.visible):                                     

                    obj = ob
        return obj
