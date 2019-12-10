import pygame
pygame.mixer.init()

sound = pygame.mixer.Sound("OOT_Song_Correct.ogg")
while True:
    sound.play()
