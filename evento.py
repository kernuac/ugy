import pygame
import tileset
import system
#Constantes
ON = 1
OFF = 0
OPENED = 1
CLOSED = 0         
class Evento(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.rect = pygame.Rect((x * 16, y * 16, dx * 16, dy * 16))
    def action(self):
        pass
        
class Teleport(Evento):
    def __init__(self, name, x, y, dx, dy, map, psx, psy, sx, sy):
        Evento.__init__(self,name, x, y, dx, dy)
        
        self.map = map
        self.psx = psx
        self.psy = psy
        self.sx = sx
        self.sy = sy
        self.type = "teleport"
    def update(self, world):
        h = world.hero
        s = world.get_stage()
        
        if h.feet.colliderect(pygame.Rect(self.rect.x - s.scrollx,
        self.rect.y - s.scrolly, self.rect.width, self.rect.height)):
            
            world.change_stage(self.map, self.sx, self.sy)
            s = world.get_stage()
            
            h.move(self.psx * 16 - h.rect.centerx - s.scrollx,
                   self.psy * 16 - h.rect.centery - s.scrolly)


class Door(Evento):
    def __init__(self, x, y, dx, dy, src, ox, oy, cx, cy, h, w, state=0):
        Evento.__init__(self, "door", x, y, dx, dy)
        til = pygame.image.load("data/"+src)
        self.images = [
            tileset.load_tile(til, cx, cy, h, w),
            tileset.load_tile(til, ox, oy, h, w)
            ]
        self.states = [CLOSED, OPENED]
        self.crrnt = state
        self.sx = 0
        self.sy = 0
        self.type = "door" 
    def get_state(self):
        return self.states[self.crrnt]
    
    def change_state(self, state):
        self.crrnt = state
    
    def action(self, scr):
        if self.get_state() == CLOSED:
            q = system.Question("Necesita contrasenia: (290 * 27)", "6930", "7830", "7430", "6830")
            k = q.update(scr)
            if k == 1:
                self.change_state(OPENED)
        #elif self.get_state() == OPENED:
        #    self.change_state(CLOSED)
    
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        if (h.feet.colliderect(pygame.Rect(self.rect.x - esc.scrollx,
        self.rect.y - esc.scrolly, self.rect.width, self.rect.height))
        and self.get_state() == CLOSED):
            h.move(h.lastx * -1, h.lasty * -1)
    
    def draw(self, scr, sx, sy):
        scr.blit(self.images[self.crrnt],
        (self.rect.x - sx, self.rect.y - sy))
class SwitchFloor(Evento):
    def __init__(self, x, y, dx, dy, src, h, w, ix, iy):
        Evento.__init__(self, "switchfloor", x, y, dx, dy)
        til = pygame.image.load("data/"+src)
        self.image = tileset.load_tile(til, ix, iy, h, w)
        self.states = [ON, OFF]
        self.crrnt = OFF
        self.sx = 0
        self.sy = 0
        self.type = "switchfloor"
    def get_state(self):
        return self.states[self.crrnt]
    def change_state(self, state):
        self.crrnt = state
    
