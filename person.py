import os
import sys
import time
import math
import datetime
from config import *
from input import *
from gen import *
from objects import *
from colorama import Back, Fore, Style


class Person:
    
    def __init__(self, h, w):
        self.height = h
        self.width = w
        # coordinates of person
        self.x = mx
        self.y = my
        self.magnet = 0
        self.gravity = 1

        self.lives = 10
        self.base = default_base
        self.roof = default_base + sc_height
        # person matrix
        self.matrix = []

    def action(self):
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
    
    def hitcheck(self, scene):
        pass


    def returnmatrix(self):
        """ Return the person as a matrix """
        return self.matrix
    
    #GRAVITY
    def fall(self, scene, ft, magnetstate):

        if magnetstate == 0:
            t = int(math.floor(0.5 * self.gravity*math.floor(ft / 5)*math.floor(ft / 5)))
            t = min(t, 4)
            t = max(t, 1)
            if self.x + 1 <= mx:
                t = min(default_base - self.x - self.height, t)
                blitobject(scene, self, self.x + t, self.y)
                self.x = self.x + t
        else:
            if self.x + 1 <= mx:
                blitobject(scene, self, self.x + 1, self.y)
                self.x = self.x + 1

# DEFINING MANDO

class Mando(Person):


    def __init__(self, height, width):
        Person.__init__(self, height, width)
        self.shield = 0
        self.shieldav = 0

        self.matrix = [[' ',Fore.LIGHTYELLOW_EX + 'O' + RESET,' '], 
                        [Fore.YELLOW + '/' + RESET,Fore.LIGHTRED_EX + '|' + RESET, Fore.YELLOW + '\\' + RESET],
                        [Fore.YELLOW + '/' + RESET,' ',Fore.YELLOW + '\\' + RESET]]
    
    
    def action(self, key, scene):
        if key == 'w' or key == 'W':
            self.gup(scene)
        elif key == 'a' or key == 'A':
            self.gleft(scene)
        elif key == 'd' or key == 'D':
            self.gright(scene)
        elif key == 's' or key == 'S':
            self.gdown(scene)
        # elif key == 'j' or key == 'J':
            # self.fire(scene)
        else:
            pass

    #ACTIONS

    def gleft(self, scene):
        if self.y > scene.scenestart() + 3:
            if self.x <= mx:
                self.pos(scene, self.x + self.gravity, self.y - 3)
            else:
                self.pos(scene, self.x, self.y - 3)
    def gright(self, scene):
        if self.y < scene.scenestart() + sc_span - 6:
            if self.x <= mx:
                self.pos(scene, self.x + self.gravity, self.y + 2)
            else:
                self.pos(scene, self.x, self.y + 2)
    def gup(self, scene):               #some glitch present. change that 2
        if self.x >= sc_top + 2:
            self.pos(scene, self.x - 2, self.y)
    
    # FIRE
    def fire(self, beam, scene):
        beam.pos(scene, beam.x, beam.y)

    # MAGNET
    def attract(self, item, scene):

        if self.x >= item.x + 4:
            self.pos(scene, self.x - 1, self.y)
        if self.y >= item.y + 4 and self.x > item.x + 4:
            self.pos(scene, self.x - 1, self.y - 1)
        elif self.y < item.y + 4 and self.x > item.x + 4:
            self.pos(scene, self.x - 1, self.y + 1)
        elif self.y > item.y + 4 and self.x <= item.x + 4:
            self.pos(scene, self.x, self.y - 1)
        elif self.y < item.y + 4 and self.x <= item.x + 4:
            self.pos(scene, self.x, self.y + 1)

    def gdown(self, scene):
        if self.x < mx - 1 and self.magnet == 1:
            self.pos(scene, self.x + 3, self.y)
    
    def getmagnet(self):
        return self.magnet

    def setmagnet(self):
        self.magnet = 1

    def unsetmagnet(self):
        self.magnet = 0

    # SHIELD

    def shieldup(self):
        self.shield = 1
        self.matrix = [['/','-','\\'], ['|',Back.YELLOW + Fore.RED + 'm' + RESET,'|'],['\\','_','/']]

    def shielddown(self):
        self.shield = 0
        self.matrix = [[' ',Fore.LIGHTYELLOW_EX + 'O' + RESET,' '], 
                        [Fore.YELLOW + '/' + RESET,Fore.LIGHTRED_EX + '|' + RESET, Fore.YELLOW + '\\' + RESET],
                        [Fore.YELLOW + '/' + RESET,' ',Fore.YELLOW + '\\' + RESET]]

    def shieldstate(self):
        return self.shield

    def shield_avnow(self):
        self.shieldav = 1
    
    def shield_unavnow(self):
        self.shieldav = 0
    
    def avstate(self):
        return self.shieldav

    def hitcheck(self, scene, coins = [], obs = []):
        scenematrix = scene.returnmatrix()
        ishit = 0
        for i in range(self.x - 1, self.x + self.height + 1):
            for j in range(self.y - 1, self.y + self.width + 1):
                if scenematrix[i][j] == '$':
                    scene.scoreadd(100)
                    for c in coins:
                        if int(c.getx()) in range(i-2,i+2) and int(c.gety()) in range(j-2,j+2):
                            scenematrix[i][j] = '#'
                            c.hit = 1
                            # break

                elif scenematrix[i][j] == '~':
                    if scene.getlives() > 0 and self.shield == 0:
                        ishit = 1
                        break
                    elif scene.getlives() > 0 and self.shield == 1:
                        self.shield_unavnow()
                        self.shielddown()   
                    
                elif scenematrix[i][j]== Fore.LIGHTCYAN_EX + 'x' + RESET:
                    for c in obs:
                        if int(c.getx()) in range(i-7,i+2) and int(c.gety()) in range(j-11,j+2):
                            scenematrix[i][j] = '#'         # can be better
                            c.hit = 1                     
                    if scene.getlives() > 0 and self.shield == 0:
                        ishit = 1
                    elif scene.getlives() > 0 and self.shield == 1:
                        self.shield_unavnow()
                        self.shielddown()
                    # elif scene.lives == 0 and self.shield == 0:
                    #     scene.lost()
                    break
        if ishit:
            scene.declives()
            if scene.getlives() == 0:
                scene.lost()

        scene.updatescene(scenematrix)

# DRAGOON

class Dragon(Person):

    def __init__(self):
        Person.__init__(self, 6, 11)
        self.lives = 6
        self.x  = mx - 15
        self.y = sc_full - 18

        self.matrix = [ ['^','_','_','^','',' ~','*','~','','',''],
                        ['(','\\','/',')','/',' ',' ',' ','\\','',''],
                        ['{','o','o','}',' ','%','$','%',' ','\\',''],
                        [' ','}','{',' ','#','~','~',' ','#',' ','|'],
                        ['(','^','^',')','/',' ',' ','\\','_','_','.'],
                        [')',' ',' ','(',' ',' ',' ',' ',' ',' ','.'] ]

    def gdown(self, scene):
        if self.x < default_base - 6:
            self.pos(scene, self.x + 3, self.y)
    def gup(self, scene):
        if self.x >= sc_top + 2:
            self.pos(scene, self.x - 2, self.y)
    def fire(self, dbeam, scene):
        dbeam.pos(scene, dbeam.x, dbeam.y)
    
    def action(self, key, scene):
        if key == 'w' or key == 'W':
            self.gup(scene)
        elif key == 's' or key == 'S':
            self.gdown(scene)
        else:
            pass
    
    def getlives(self):
        return self.lives
    
    def sublives(self):
        self.lives -= 1


    def hitcheck(self, scene):
        scenematrix = scene.returnmatrix()
        for i in range(self.x - 1, self.x + self.height + 1):
            for j in range(self.y - 2, self.y + 2):
                if scenematrix[i][j] == ']':
                    if self.lives > 0:
                        self.lives -= 1
                        break
                    else:
                        scene.scoreadd(4000)
                        scene.won()
        
        scene.updatescene(scenematrix)