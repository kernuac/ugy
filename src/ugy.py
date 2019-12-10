#!/usr/bin/python -OO
import pygame
import aplicacion 
import sys

def main(argv):
    """Funcion principal"""
    pygame.init()
    pygame.mixer.init()
    ap = aplicacion.Aplicacion(0)
    ap.loop()
    pygame.quit()

if __name__=="__main__": main(sys.argv)
    
