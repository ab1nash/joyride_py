from person import *
from scene import *
import random

class Magnet(Person):

    def __init__(self, scene):
        self.height = 4
        self.width = 4
        self.x = sc_top + 2
        self.y = random.randint(scene.scenestart(), scene.scenestart() + sc_span - 4)
        self.matrix = [[' ','-','-',' '],['/',' ',' ','\\'],['/',' ',' ','\\'],['U',' ',' ','U']]