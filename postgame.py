import sys
import os
import time
from scene import *
from config import *



def lscr(scene):
    sceneprint = ""
    sceneprint += colors['Red'] + " "*40 + "YOU LOST. KEEP TRYING !\n" + RESET
    sceneprint += '\n'
    sceneprint += " "*40 + "YOUR SCORE IS " + RESET
    sceneprint += str(scene.getscore())

    print(sceneprint)
    time.sleep(1)

def wscr(scene):
    sceneprint = ""
    sceneprint += colors['lGreen'] + " "*40 + "YOU WIN. HOORAY!\n" + RESET
    sceneprint += '\n'
    sceneprint += " "*40 + "YOUR SCORE IS " + RESET
    sceneprint += str(scene.getscore())

    print(sceneprint)
    time.sleep(1)