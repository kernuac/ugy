import pygame
from pygame.locals import K_DOWN, K_UP, K_RETURN, KEYDOWN
BLACK = (0,0,0)
RED = (255,0,0)


class Question:
    def __init__(self, qs, *ans ):
        self.question = qs
        self.answers = ans
        self.opt = 0
        self.img = None
        self.font = pygame.font.Font(None, 25)
    
    def update(self, scr):
        resp = False
        while not resp:
            for e in pygame.event.get([KEYDOWN]):
                if e.key == K_DOWN and self.opt < len(self.answers):
                    self.opt += 1
                    print "down"
                if e.key == K_UP and self.opt > 0:
                    self.opt -= 1
                if e.key == K_RETURN:
                    k = self.opt
                    resp = True
                                    
            self.show(scr, 20,96)
            pygame.display.update()
        return k
    
    def show(self,scr, x, y):
        a = []
        bx = pygame.image.load("data/BigBox.png").convert()
        bx.set_colorkey((255,0,255))
        bxrect = bx.get_rect()
        #bxrect.x = x
        #bxrect.y = y
        cnt = 1
        q = self.font.render(self.question, True, BLACK)
        scr.blit(bx,(x,y))
        scr.blit(q,(x + 16, y + 16 * cnt))
        cnt += 1
        for i in range(len(self.answers)):
            if i == self.opt:
                a.append(self.font.render("> "+self.answers[i],True,RED))
            else:
                a.append(self.font.render(self.answers[i],True,BLACK))

        for text in a:
            scr.blit(text,(x + 16, y + 16 * cnt))
            cnt += 1

class Action:
    def __init__(self):
        self.action = ""
        self.font = pygame.font.Font(None, 25)
    
    def show(self, scr, x, y):
        sp = pygame.image.load("data/Space.png").convert()
        sp.set_colorkey((255,0,255))
        scr.blit(sp, (x, y))
        tx = self.font.render(self.action, True, BLACK)
        scr.blit(tx, (x + 8, y + 8))
        
    def set_action(self, action):
        self.action = action
