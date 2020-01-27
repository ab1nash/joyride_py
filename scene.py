from config import *
import sys
import math

class Scene:
    
    def __init__(self, height, width, fullwidth):
        self.__base = default_base
        self.__roof = None
        self.__height = height
        self.__width = width
        self.__fullwidth = fullwidth
        self.__start = 0
        self.__ct = 0
        self.__score = 0
        self.__gameover = 0
        self.__lives = 20
        self.__timetog = 0.15
        self.__remaining_time = sc_time
        self.__matrix = []

        # Making an empty matrix
        for x in range(0, sc_full):
            self.__matrix.append([])
            for y in range(0, sc_full):
                self.__matrix[x].append(' ')

        for x in range(default_base, sc_height):
            for y in range(0, sc_full):
                self.__matrix[x][y] = colors['lGreen'] + '#' + RESET

        for x in range(2, sc_top):
            for y in range(0, sc_full, 2):
                self.__matrix[x][y] = colors['lGreen'] + '>' + RESET
    
    def displayScene(self):                                                 
        """ Print the screen to the terminal """
        sceneprint = ""
        sceneprint += " "*40 + Back.LIGHTRED_EX + Fore.LIGHTCYAN_EX + Style.BRIGHT + "M A N D A L O R I A N\n" + RESET
        sceneprint += Fore.LIGHTBLUE_EX +"SCORE : " +\
            str(self.__score) + " "*30 +"TIME : " + str(self.__remaining_time) + " "*30 +\
            "LIVES:" + str(self.__lives)+"\n"+ RESET
        if self.__start >= self.__fullwidth - self.__width:
            self.__start = self.__fullwidth - self.__width
        for i in range(0, self.__height):
            for j in range(self.__start, self.__start + self.__width):
                sceneprint += str(self.__matrix[i][j])
            sceneprint += '\n'
        
        if self.__start + sc_span < sc_full - 5:
            self.__start = self.__start + 1
            if self.__score < 420420420:
                self.__score += 1
                pass

        return sceneprint
    
    def scenetimeset(self, t):
        self.__remaining_time -= t
        self.__remaining_time = math.ceil(self.__remaining_time)

    def returnmatrix(self):
        return self.__matrix

    def updatescene(self, updmatrix):
        self.__matrix = updmatrix
    
    def scenestart(self):
        return self.__start

    def isover(self):
        return self.__gameover

    def lost(self):
        self.__gameover = 1
    
    def won(self):
        self.__gameover = 2
    
    def getlives(self):
        return self.__lives
    
    def declives(self):
        self.__lives -= 1
    
    def getscore(self):
        return self.__score
    
    def scoreadd(self,val):
        self.__score += val

    def timetoggle(self):
        if self.__timetog == 0.15:
            self.__timetog = 0.06
        else:
            self.__timetog = 0.15
    
    def getspeed(self):
        return self.__timetog

    def getremtime(self):
        return self.__remaining_time