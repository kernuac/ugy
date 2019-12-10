import pygame
import tileset
import system
import os
import mathematics
import random
import window
import music
import time
from pprint import pprint

#Constantes
ON = 1
OFF = 0
OPENED = 1
CLOSED = 0
DERECHA = 1
IZQUIERDA = 0
JOIN = os.path.join
PATH = os.path.abspath(os.path.dirname(__file__))
DATA = JOIN(PATH, "data")

class Evento(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dx, dy, required):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.rect = pygame.Rect((x * 16, y * 16, dx * 16, dy * 16))
        self.required = required
        self.visible = True
        if self.required == "None":
            self.required = None
    def action(self, wd):
        pass
        
    def change_state(self, state):
        self.crrnt = state
        
    def get_state(self):
        return self.states[self.crrnt]
    
    def check_event(self, events):
        op = False
        for e in events.sprites():
            if self.required != None:
                if e.name == self.required:
                    if e.get_state() == 1:
                        op = True
                    else: 
                        op = False
            else: op = True
        return op

class Teleport(Evento):
    def __init__(self, name, x, y, dx, dy, map, psx, psy, sx, sy, req):
        Evento.__init__(self,name, x, y, dx, dy, req)
        
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
    def __init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req):
        Evento.__init__(self, name, x, y, dx, dy, req)
        til = pygame.image.load(JOIN(DATA, src))
        self.images = [
            tileset.load_tile(til, cx, cy, h, w),
            tileset.load_tile(til, ox, oy, h, w)
            ]
        self.states = [CLOSED, OPENED]
        self.crrnt = CLOSED
        self.sx = 0
        self.sy = 0
        self.type = "door" 
    
    def action(self, events):
        if self.check_event(events):
            if self.get_state() == CLOSED:
                self.change_state(OPENED)
                music.DOOR_OPEN.play() 
                
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
        if exists:
            if (h.feet.colliderect(pygame.Rect(self.rect.x - esc.scrollx,
            self.rect.y - esc.scrolly, self.rect.width, self.rect.height))
            and self.get_state() == CLOSED):
                h.move(h.lastx * -1, h.lasty * -1)
    
    def draw(self, sx, sy):
        window.scr.blit(self.images[self.crrnt],
        (self.rect.x - sx, self.rect.y - sy))

class KeyDoor(Door):
    def __init__(self, name, x, y, dx, dy, src, 
                     ox, oy, cx, cy, h, w, req):
        Door.__init__(self, name, x, y, dx, dy, src, 
                           ox, oy, cx, cy, h, w, req)
        self.key = False

    def action(self, events):
        if self.check_event(events):
            if self.get_state() == CLOSED and self.key:
                self.change_state(OPENED)
                music.DOOR_OPEN.play()
            elif not self.key:
                ms = system.Message("Necesitas una llave para abrirla")
                ms.update()
                
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        
        
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
                
        if exists:
            if (h.feet.colliderect(pygame.Rect(self.rect.x - esc.scrollx,
            self.rect.y - esc.scrolly, self.rect.width, self.rect.height))
            and self.get_state() == CLOSED):
                if wd.hero.has_item("key") and not self.key:
                    wd.hero.del_item("key")
                    music.OK.play()
                    self.key = True
                h.move(h.lastx * -1, h.lasty * -1)
                
class DoorPasswd(Door):
    def __init__(self, name, x, y, dx, dy, src, 
                     ox, oy, cx, cy, h, w, req):
        Door.__init__(self, name, x, y, dx, dy, src, 
                           ox, oy, cx, cy, h, w, req)   
        self.excercise = mathematics.type[random.randint(0,7)]()
        self.text = "La puerta requiere una contrasenia,\npuedes deducirla ?"
        
    def action(self, events):
        ms = system.Excercise(self.text, self.excercise.exc)
        op = ms.update()
        if self.excercise.check_ans(op):
            self.change_state(OPENED)
            music.DOOR_OPEN.play()

class ButtonFloor(Evento):
    def __init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req):
        Evento.__init__(self, name, x, y, dx, dy, req)
        til = pygame.image.load(JOIN(DATA, src))
        self.images = [
                        tileset.load_tile(til, cx, cy, h, w),
                        tileset.load_tile(til, ox, oy, h, w)
                      ]
        self.states = [OFF, ON]
        self.crrnt = OFF
        self.sx = 0
        self.sy = 0
        self.type = "ButtonFloor"
    
    def action(self, eventos):
        if self.check_event(eventos):
            if self.get_state() == OFF:
                self.change_state(ON)
                music.BUTTON.play()
    
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
        if exists:
            if (h.feet.colliderect(pygame.Rect(self.rect.x - esc.scrollx,
            self.rect.y - esc.scrolly, self.rect.width, self.rect.height))):
                self.action(esc.eventos[1])
                h.move(h.lastx * -1, h.lasty * -1)
             
    def draw(self, sx, sy):
        window.scr.blit(self.images[self.crrnt],
        (self.rect.x - sx, self.rect.y - sy))
        
class ButtonFloorMath(ButtonFloor):
    def __init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req):
        ButtonFloor.__init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req)
        self.excercise = mathematics.type[random.randint(0,7)]()
        self.text = " Para activar este boton, \n debes decirme cuanto es" 
    
    def action(self, eventos):
        if self.check_event(eventos):
            if self.get_state() == OFF:
                ms = system.Excercise(self.text,self.excercise.exc)
                op = ms.update()
                if self.excercise.check_ans(op):
                    self.change_state(ON)
                    music.BUTTON.play()

class SwitchFloor(Evento):
    def __init__(self, name, x, y, dx, dy, src, drx, dry, izx, izy, h, w, req):
        Evento.__init__(self, name, x, y, dx, dy, req)
        til = pygame.image.load(JOIN(DATA,src))
        self.images = [
                        tileset.load_tile(til, drx, dry, h, w),
                        tileset.load_tile(til, izx, izy, h, w)
                      ]
        self.states = [IZQUIERDA, DERECHA]
        self.crrnt = IZQUIERDA
        self.sx = 0
        self.sy = 0
        self.type = "switchfloor"
    
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
        if exists:
            if (h.feet.colliderect(pygame.Rect(self.rect.x + 1 - esc.scrollx,
            self.rect.y + 1 - esc.scrolly, self.rect.width, self.rect.height))):
                h.move(h.lastx * -1, h.lasty * -1)
            
    def action(self, events):
        if self.required == None:
            if self.get_state() == DERECHA:
                self.change_state(IZQUIERDA)
                music.SWITCH.play()
            else:
                self.change_state(DERECHA)
                music.SWITCH.play()
        else:
            if self.check_event(events):
                if self.get_state() == DERECHA:
                    self.change_state(IZQUIERDA)
                    music.SWITCH.play()
                else:
                    self.change_state(DERECHA)
                    music.SWITCH.play()
            else:
                ms = system.Message("Aun no puedes usar esto")
                ms.update()
                
    def draw(self, sx, sy):
        window.scr.blit(self.images[self.crrnt],
        (self.rect.x - sx, self.rect.y - sy))

class SwitchFloorMath(SwitchFloor):
    def __init__(self, name, x, y, dx, dy, 
        src, drx, dry, izx, izy, h, w, req):
        SwitchFloor.__init__(self, name, x, y, dx, dy,
        src, drx, dry, izx, izy, h, w, req)
        self.excercise = None
        self.text = "Si deseas manipular este switch,\ndeberas responder correctamente:"
        
    def action(self, events):
        self.excercise = mathematics.type[random.randint(0,7)]()
        if self.required == None:
            ms = system.Excercise(self.text,self.excercise.exc)
            op = ms.update()
            if self.excercise.check_ans(op):
                if self.get_state() == DERECHA:
                    self.change_state(IZQUIERDA)
                    music.SWITCH.play()
                else:
                    self.change_state(DERECHA)
                    music.SWITCH.play()
        else:
            if self.check_event(events):
                ms = system.Excercise(self.text,self.excercise.exc)
                op = ms.update()
                if self.excercise.check_ans(op):
                    if self.get_state() == DERECHA:
                        self.change_state(IZQUIERDA)
                        music.SWITCH.play()
                    else:
                        self.change_state(DERECHA)
                        music.SWITCH.play()
            else:
                ms = system.Message("No puedes utilizar esto aun")
                ms.update()

class Block(Evento):
    def __init__(self, name, x, y, dx, dy, src, ix, iy, h, w, req):
        Evento.__init__(self, name, x, y, dx, dy, req)
        til = pygame.image.load(JOIN(DATA, src))
        self.image = tileset.load_tile(til, ix, iy, h, w)
        self.sx = 0
        self.sy = 0
        self.type = "Block"
        self.states = [0,1]
        self.crrnt = 0
        self.visible = True
        
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
        if exists:
            if self.required != None and self.check_event(esc.eventos[1]):
                if self.visible:
                    music.WALL_DOWN.play()
                self.visible = False
            else:
                self.visible = True
                if(h.feet.colliderect(pygame.Rect(self.rect.x + 1 - esc.scrollx,
                self.rect.y + 1 - esc.scrolly, self.rect.width,
                self.rect.height))):
                    h.move(h.lastx * -1, h.lasty * -1)
                    ms = system.Message("No puedes pasar !!")
                    ms.update()
    
    def draw(self, sx, sy):
        if self.visible:
            window.scr.blit(self.image, 
            (self.rect.x - sx, self.rect.y - sy))
            

class KeyBlock(Block):
    def __init__(self, name, x, y, dx, dy, src, ix, iy, h, w, req):
        Block.__init__(self, name, x, y, dx, dy, src, ix, iy, h, w, req)
        self.key = False
        self.states = [CLOSED, OPENED]
        self.crrnt = CLOSED
        self.type = "keyblock"

    def action(self, events):
        if self.check_event(events):
            if self.get_state() == CLOSED and self.key:
                self.change_state(OPENED)
                self.visible = False
                music.WALL_DOWN.play() 
            elif not self.key:
                ms = system.Message("Este muro parece requerir una llave...")
                ms.update()
                
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
                
        if exists:
            if (h.feet.colliderect(pygame.Rect(self.rect.x - esc.scrollx,
            self.rect.y - esc.scrolly, self.rect.width, self.rect.height))
            and self.get_state() == CLOSED):
                ms = system.Message("No puedes pasar !!")
                h.move(h.lastx * -1, h.lasty * -1)
                
                if wd.hero.has_item("key") and not self.key:
                    wd.hero.del_item("key")
                    music.OK.play()
                    self.key = True
                
class Chest(Evento):
    def __init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req, item):
        Evento.__init__(self, name, x, y, dx, dy, req)
        til = pygame.image.load(JOIN(DATA, src))
        self.images = [
                        tileset.load_tile(til, cx, cy, h, w),
                        tileset.load_tile(til, ox, oy, h, w)
                      ]
        self.states = [CLOSED, OPENED]
        self.crrnt = CLOSED
        self.sx = 0
        self.sy = 0
        self.type = "chest"
        self.item = item
        self.visible = True
        if self.required != None:
            self.visible = False
            
    def update(self, wd):
        h = wd.hero
        esc = wd.get_stage()
        exists = False
        for ob in iter(esc.eventos[1]):
            if ob == self:
                exists = True
        if exists:
            if self.check_event(esc.eventos[1]) and self.required != None:
                self.visible = False
            else:
                self.visible = True
                if(h.feet.colliderect(pygame.Rect(self.rect.x + 1 - esc.scrollx,
                self.rect.y + 1 - esc.scrolly, self.rect.width,
                self.rect.height))):
                    h.move(h.lastx * -1, h.lasty * -1)
        if self.item != None and self.get_state() == OPENED:
            h.get_item(self.item)
            if self.item == "None":
                item = " Nada"
            else:
                item = " 1 " + self.item
            ms = system.Message("Has obtenido"+item+" !!")
            music.GOT_ITEM.play()
            ms.update()
            self.item = None
    
    def action(self, eventos):
        if self.visible:
            if self.get_state() == CLOSED:
                self.change_state(OPENED)
                music.CHEST_OPEN.play()
                time.sleep(1.0)
                                   
    def draw(self, sx, sy):
        if self.visible:
            window.scr.blit(self.images[self.crrnt], 
            (self.rect.x - sx, self.rect.y - sy))

class ChestPasswd(Chest):
    def __init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req, item):
        Chest.__init__(self, name, x, y, dx, dy, src, ox, oy, cx, cy, h, w, req, item)
        self.excercise = mathematics.type[random.randint(0,7)]()
        self.text = " Puedes deducir esta clave "
    def action(self, eventos):
        if self.visible:
            if self.get_state() == CLOSED:
                ms = system.Message("Este cofre necesita una clave")
                ms.update()
                ms = system.Excercise(self.text, self.excercise.exc)
                op = ms.update()
                if self.excercise.check_ans(op):
                    self.change_state(OPENED)
                    music.CHEST_OPEN.play()
                    time.sleep(1.0)
