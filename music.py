import pygame
import os
JOIN = os.path.join
PATH = os.path.abspath(os.path.dirname(__file__))
DATA = JOIN(PATH, "data")

pygame.mixer.init()
LOAD_SND = pygame.mixer.Sound
MUSIC = pygame.mixer.music
BUTTON = LOAD_SND(JOIN(DATA, "OOT_Switch.ogg"))        
DOOR_OPEN = LOAD_SND(JOIN(DATA, "OOT_Door_Regular_Open.ogg"))
DOOR_CLOSE = LOAD_SND(JOIN(DATA, "OOT_Door_Regular_Close.ogg"))
ERROR = LOAD_SND(JOIN(DATA, "OOT_Error.ogg"))
OK = LOAD_SND(JOIN(DATA, "OOT_Song_Correct.ogg"))
DIALOG_OPEN = LOAD_SND(JOIN(DATA, "TP_Dialogue_Open.ogg"))
DIALOG_CLOSE = LOAD_SND(JOIN(DATA, "TP_Dialogue_Close.ogg"))
KEY = LOAD_SND(JOIN(DATA, "OOT_MainMenu_Letter.ogg"))
CHEST_OPEN = LOAD_SND(JOIN(DATA, "OOT_Chest_Small.ogg"))
GOT_ITEM = LOAD_SND(JOIN(DATA, "OOT_Fanfare_SmallItem.ogg"))
SWITCH = LOAD_SND(JOIN(DATA, "SwitchFloor.ogg"))
WALL_DOWN = LOAD_SND(JOIN(DATA, "OOT_Bomb_Blow.ogg"))
MUSIC.load(JOIN(DATA, "MinishVillageXGv1-2.mid"))

def change_music(music):
    MUSIC.stop()
    MUSIC.load(JOIN(DATA, music))
    
