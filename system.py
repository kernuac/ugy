import pygame
import os
import window
import string
import music
import time
import tileset
from pygame.locals import K_DOWN, K_UP, K_RETURN, KEYDOWN, K_BACKSPACE
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
JOIN = os.path.join
PATH = os.path.abspath(os.path.dirname(__file__))
DATA = JOIN(PATH, "data")
KEY = tileset.load_tile(pygame.image.load(JOIN(DATA, "Inner-Castle-13.png")).convert(),
                            464, 208, 16, 16)
KEY.set_colorkey((255,0,255))
class Message:
    def __init__(self, txt):
        self.text = txt
        self.font = pygame.font.Font(JOIN(DATA, "T4C Beaulieux.ttf"), 18)
        
    def update(self):
        done = False
        music.MUSIC.set_volume(0.3)
        time.sleep(1.0)
        music.DIALOG_OPEN.play()
        while not done:
            #for e in pygame.event.get([KEYDOWN]):
            event = pygame.event.wait()
            print event.type
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    done = True
            self.show(20, 96)
            pygame.display.update()
        music.DIALOG_CLOSE.play()
        time.sleep(1.0)
        music.MUSIC.set_volume(1.0)
        
    def show(self, x, y):
        bx = pygame.image.load(JOIN(DATA, "BigBox.png")).convert()
        bx.set_colorkey((255, 0, 255))
        bxrect = bx.get_rect()
        txt = self.font.render(self.text, True, BLACK)
        window.scr.blit(bx, (x, y))
        window.scr.blit(txt, (x + 16, y + 16))
        
class Question:
    def __init__(self, qs, *ans ):
        self.question = qs
        self.answers = ans
        self.opt = 0
        self.img = None
        self.font = pygame.font.Font(JOIN(DATA, "T4C Beaulieux.ttf"), 18)
    
    def update(self):
        resp = False
        music.MUSIC.set_volume(0.3)
        time.sleep(1.0)
        music.DIALOG_OPEN.play()
        clock = pygame.time.Clock()
        while not resp:
            #for e in pygame.event.get([KEYDOWN]):
            event = pygame.event.wait()
            print event.type
            if event.type == KEYDOWN:
                if event.key == K_DOWN and self.opt < len(self.answers):
                    self.opt += 1
                if event.key == K_UP and self.opt > 0:
                    self.opt -= 1
                if event.key == K_RETURN:
                    k = self.opt
                    resp = True
                                    
            self.show(20, 96)
            pygame.display.update()
            pygame.display.update()
        music.DIALOG_CLOSE.play()
        time.sleep(1.0)
        music.MUSIC.set_volume(1.0)
        return k
    
    def show(self, x, y):
        a = []
        bx = pygame.image.load(JOIN(DATA,"BigBox.png")).convert()
        bx.set_colorkey((255,0,255))
        bxrect = bx.get_rect()
        cnt = 1
        q = self.font.render(self.question, True, BLACK)
        window.scr.blit(bx,(x,y))
        window.scr.blit(q,(x + 16, y + 16 * cnt))
        cnt += 1
        for i in range(len(self.answers)):
            if i == self.opt:
                a.append(self.font.render("> "+self.answers[i],True,RED))
            else:
                a.append(self.font.render(self.answers[i],True,BLACK))

        for text in a:
            window.scr.blit(text,(x + 16, y + 16 * cnt))
            cnt += 1
            
class Excercise:
    def __init__(self,question, exc):
        self.excercise = exc
        self.question = question
        self.font = pygame.font.Font(JOIN(DATA, "T4C Beaulieux.ttf"), 18)
    def update(self):
        done = False
        text = ""
        resp = None
        music.MUSIC.set_volume(0.3)
        music.DIALOG_OPEN.play()
        clock = pygame.time.Clock()
        while not done:
            #for e in pygame.event.get([KEYDOWN]):
            event = pygame.event.wait()
            print event.type
            if event.type == KEYDOWN:
                print "presionamos la tecla"
                music.KEY.play()
                if event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key == K_RETURN:
                    try:
                        resp = int(text)
                    except:
                        resp = None
                    done = True
                else:
                    k = pygame.key.name(event.key)
                    if not len(k) > 3:
                        if len(k) == 3:
                            k = k[1:-1]
                        if len(text) < 7:
                            text += k
            self.show(20, 96, self.question, text)
            pygame.display.update()
            clock.tick(20)
        music.DIALOG_CLOSE.play()
        music.MUSIC.set_volume(1.0)
        return resp    

    def show(self, x, y, question, text):
        bx = pygame.image.load(JOIN(DATA, "BigBox.png")).convert()
        bx.set_colorkey((255,0,255))
        bxrect = bx.get_rect()
        question = question.split("\n")
        ex = self.font.render(self.excercise, True, BLACK)
        rp = self.font.render(text+"|", True, BLACK)
        cnt = 1
        window.scr.blit(bx,(x + 16, y + 20 * cnt))
        cnt += 1
        for t in question:
            q = self.font.render(t, True, BLACK)
            window.scr.blit(q,(x + 25, y + 20 * cnt))
            cnt += 1
        window.scr.blit(ex,(x + 25, y + 20 * cnt))
        cnt += 1
        window.scr.blit(rp, (x + 25, y + 20 * cnt))

class Key:
    def __init__(self):
        self.font = pygame.font.Font(JOIN(DATA, "T4C Beaulieux.ttf"), 18)
        self.keys = ""
        
    def show(self, x, y):
        keys = self.font.render("x "+self.keys, True, WHITE)
        window.scr.blit(KEY, (x, y))
        window.scr.blit(keys, (x + 20, y))
        
    def set_cnt_keys(self, keys):
        self.keys = str(keys)
        
class Action:
    def __init__(self):
        self.action = "0"
        self.font = pygame.font.Font(JOIN(DATA, "T4C Beaulieux.ttf"), 18)
    
    def show(self, x, y):
        sp = pygame.image.load(JOIN(DATA,"Space.png")).convert()
        sp.set_colorkey((255,0,255))
        window.scr.blit(sp, (x, y))
        tx = self.font.render(self.action, True, BLACK)
        window.scr.blit(tx, (x + 8, y + 8))
        
    def set_action(self, action):
        self.action = action
