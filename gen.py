import os
import sys
import time
from config import *
from input import *
from colorama import Back, Fore, Style

def show_title_page():
    os.system('clear')
    print(Fore.RED+Style.BRIGHT+"MANDALORIAN!!")
    time.sleep(1)
    os.system('clear')

def blitobject(scene, item, x, y):
    
    """ Blit given item over the scene where 
    specified after deleting previous instance"""
    
    scenematrix = scene.returnmatrix()
    itemmatrix = item.returnmatrix()

    # deleting previous position
    for i in range(item.getx(), item.getx() + item.getheight()):
        for j in range(item.gety(), item.gety() + item.getwidth()):
            scenematrix[i][j] = ' '

    # putting at new position
    for i in range(x, x + item.getheight()):                       #fixed
        for j in range(y, y + item.getwidth()):
            scenematrix[i][j] = itemmatrix[i-x][j-y]

    scene.updatescene(scenematrix)

def deletematrix(scene, item):

    '''Delete the <item> from the <scene>'''
    scenematrix = scene.returnmatrix()
    for i in range(item.getx(), item.getx() + item.getheight()):
        for j in range(item.gety(), item.gety() + item.getwidth()):
            scenematrix[i][j] = ' '
    scene.updatescene(scenematrix)