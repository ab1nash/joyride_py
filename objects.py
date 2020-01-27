import os
import sys
import time
from config import *
from input import *
from gen import *
from scene import *
# from person import *
from colorama import Back, Fore, Style

class Object:
    
    def __init__(self, h, w):
        self.height = h
        self.width = w
        # coordinates of Object
        self.x = sc_height - 12
        self.y = sc_full - 40
        self.gravity = 1
        self.base = default_base
        self.roof = default_base + sc_height
        # Object matrix
        self.matrix = []

    def action(self):
        pass

    def hitcheck(self):
        pass

    def getx(self):
        return self.x

    def gety(self):
        return self.y
    
    def getheight(self):
        return self.height
    
    def getwidth(self):
        return self.width

    def pos(self, scene, x, y):
        """ Calls blitobject function and updates position """
        blitobject(scene, self, x, y)
        self.x = x
        self.y = y
    
    def returnmatrix(self):
        """ Return the Object as a matrix """
        return self.matrix
    
class Coin(Object):

    # p = colors['Yellow'] + '$' + RESET

    def __init__(self, scene, x):
        self.height = 1
        self.width = 1
        self.hit = 0
        # coordinates of coin
        self.x = x
        self.y = min(scene.scenestart() + sc_span + 4, sc_full - 120)
        self.matrix = ['$']

class Obs(Object):
    
    def hitcheck(self, scene, beams = []):
        # for beam
        scenematrix = scene.returnmatrix()
        trigger = 0
        for i in range(1,4):
            for j in range(self.x, self.x + self.height):
                if scenematrix[j][self.y - i] == ']':
                    trigger = 1
                    #delete beam  //fixed//
                    for k in beams:
                        if k.y == self.y - i  and k.x == j:
                            scenematrix[j][self.y - i] = 'O'
                            k.hit = 1

                    #delete obstacle
                    for a in range(self.x, self.x+self.height):
                        for b in range(self.y, self.y+self.width):
                            scenematrix[a][b] = ' '
            if trigger:
                self.hit = 1
                # break
        scene.updatescene(scenematrix)
 
        # for mandalorian
            # is in mando's class because easier.
    


class Vbeam(Obs):

    def __init__(self, scene, x):
        self.height = 6
        self.width = 1
        self.hit = 0
        # coordinates
        self.x = x
        self.y = min(scene.scenestart() + sc_span + 8, sc_full - 120)
        self.matrix = [[Fore.LIGHTCYAN_EX + 'x' + RESET],[Fore.LIGHTCYAN_EX + 'x' + RESET],[Fore.LIGHTCYAN_EX + 'x' + RESET],
        [Fore.LIGHTCYAN_EX + 'x' + RESET],[Fore.LIGHTCYAN_EX + 'x' + RESET],[Fore.LIGHTCYAN_EX + 'x' + RESET]]

class Hbeam(Obs):

    def __init__(self, scene, x):
        self.height = 1
        self.width = 11
        self.hit = 0
        # coordinates
        self.x = x
        self.y = min(scene.scenestart() + sc_span + 8, sc_full - 120)
        self.matrix = [[Fore.LIGHTCYAN_EX + 'x' + RESET,' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',Fore.LIGHTCYAN_EX + 'x' + RESET]]

class Ldbeam(Obs):

    def __init__(self, scene, x):
        self.height = 6
        self.width = 6
        self.hit = 0
        # coordinates
        self.x = x
        self.y = min(scene.scenestart() + sc_span + 8, sc_full - 120)
        self.matrix = [
        [Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' ',' ',' ',' '],
        [' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' ',' ',' '],
        [' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' ',' '],
        [' ',' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' '],
        [' ',' ',' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' '],
        [' ',' ',' ',' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET]]

class Rdbeam(Obs):


    def __init__(self, scene, x):
        self.height = 6
        self.width = 6
        self.hit = 0
        self.matrix = []
        # coordinates
        self.x = x
        self.y = min(scene.scenestart() + sc_span + 8, sc_full - 120)
        self.matrix = [
        [' ',' ',' ',' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET],
        [' ',' ',' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' '],
        [' ',' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' '],
        [' ',' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' ',' '],
        [' ',Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' ',' ',' '],
        [Fore.LIGHTCYAN_EX + 'x' + RESET,' ',' ',' ',' ',' ']]

        
# Note : Beam, Mando and boss will check for collision with characters.

class Beam(Object):

    def __init__(self, scene, x, y):
        self.height = 1
        self.width = 1
        # coordinates of coin
        self.x = x
        self.y = y
        self.hit = 0
        self.matrix = [']']

    def hitcheck(self, scene):
    # for obstacle
        scenematrix = scene.returnmatrix()
        for i in range(1,4):
            if scene.matrix[self.y + i] == 'x':
                #delete beam

                #delete obstacle
                a = self.y - 3          # y
                b = min(self.x - 6, 1)  # x
                for i in range (b, b + 20):
                    for j in range (a, a + 20):
                        if scenematrix[i][j] == 'x':
                            scenematrix[i][j] = '2'
                        
                scene.updatescene(scenematrix)
                scene.returnmatrix()

class dBeam(Object):

    def __init__(self, scene, x, y):
        self.height = 1
        self.width = 1
        self.x = x
        self.y = y
        self.hit = 0
        self.matrix = ['~']