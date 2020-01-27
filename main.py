#!/usr/bin/env python3

import os
import sys
import time
import cursor
import datetime
import random
from config import *
from input import *
from gen import *
from scene import *
from person import *
from objects import *
from magnet import *
from postgame import *
from colorama import Back, Fore, Style

show_title_page()
cursor.hide()
getinp = Get()
scene = Scene(sc_height, sc_span, sc_full)
mando = Mando(mando_h, mando_w)  # fill the x,y
beamval = 0
bosstime = 0
beams = []
dbeams = []
coins = []
obs = []
falltime = 9

# setting our Mando up
mando.pos(scene, mx, my)
mando.shield_avnow()

boss = Dragon()
print(scene.displayScene())
timest = datetime.datetime.now()
gametime = timest

while True:

    if scene.isover() == 1:
        os.system('clear')    
        lscr(scene)
        break
    elif scene.isover() == 2:
        os.system('clear')
        wscr(scene)
        break

    timenow = datetime.datetime.now()
    elapsedtime = timenow - timest
    elapsedgt = timenow - gametime
    # [TODO] make time consistent
    elsec = (elapsedgt.seconds) / 20 + 1
    scene.scenetimeset(elsec)
    if scene.getremtime() == 0:
        os.system('clear')    
        lscr(scene)
        break

    time.sleep(1/140)
    input = input_to(getinp, scene.getspeed())
    os.system('clear')

    #SHIELD

    

    if elapsedtime.seconds >= 10 and mando.shieldstate() == 1:
        mando.shield_unavnow()
        timest = datetime.datetime.now()
        mando.shielddown()
    elif elapsedtime.seconds >= 60 and mando.shieldstate() == 0:
        mando.shield_avnow()
        timest = datetime.datetime.now()

        
    

    spawn = random.randint(0,300)
    if scene.scenestart() < sc_full - sc_span * 2 - 20:
        if spawn > 250:
            coins.append(Coin(scene, random.randint(sc_top,default_base - 1)))
            k = len(coins)-1
            coins[k].pos(scene, coins[k].getx(), coins[k].gety())
        elif spawn in range(10,14):
            obs.append(Vbeam(scene, random.randint(sc_top + 2,default_base - 7)))
            obs[len(obs)-1].pos(scene, obs[len(obs)-1].getx(), obs[len(obs)-1].gety())
        elif spawn in range(16,20):
            obs.append(Hbeam(scene, random.randint(sc_top + 2,default_base - 7)))
            obs[len(obs)-1].pos(scene, obs[len(obs)-1].getx(), obs[len(obs)-1].gety())
        elif spawn in range(22,26):
            obs.append(Ldbeam(scene, random.randint(sc_top + 2,default_base - 7)))
            obs[len(obs)-1].pos(scene, obs[len(obs)-1].getx(), obs[len(obs)-1].gety())
        elif spawn in range(200,204):
            obs.append(Rdbeam(scene, random.randint(sc_top + 2,default_base - 7)))
            obs[len(obs)-1].pos(scene, obs[len(obs)-1].getx(), obs[len(obs)-1].gety())

    #BOSS
    
    if scene.scenestart() >= sc_full - sc_span - 10 and bosstime == 0:
        bosstime = 1
        boss.pos(scene, sc_height - 20, sc_full - 15)
    
    if random.randint(0,5) == 1 and bosstime == 1:
        dbeams.append(dBeam(scene, boss.x + 4, boss.y - 2))
        boss.fire(dbeams[len(dbeams)-1], scene)
    
    if bosstime == 1:
        boss.hitcheck(scene)

    #MAGNET

    if random.randint(0,1000) == 1 and mando.getmagnet() == 0 and scene.scenestart() <= sc_full - sc_span - 10:
        mando.setmagnet()
        start = datetime.datetime.now()
        magnet = Magnet(scene)
        magnet.pos(scene, magnet.x, magnet.y)

    #MANDO ACTION

    if input is not None:
        falltime = 9
        if input == 'j' or input == 'J':
            beamval = 1
            beams.append(Beam(scene, mando.x + 1, mando.y + 4))
            mando.fire(beams[len(beams)-1], scene)
        elif input == ' ' and mando.avstate() == 1:
            timest = datetime.datetime.now()
            mando.shieldup()
        elif input == 't' or input == 'T':
            scene.timetoggle()
        else:
            mando.action(input, scene)
            if random.randint(0,1) == 1:
                boss.action(input, scene)

    # exit
        if input == 'q' or input == 'Q':
            os.system('clear')
            sys.exit()
    
    else:
        falltime = falltime + 1
        mando.fall(scene, falltime, mando.getmagnet())
        if bosstime == 1:
            if random.randint(0,10) > 1 and boss.x + 6 < default_base - 1:
                boss.fall(scene, falltime, 0)


    if scene.scenestart() + sc_span < sc_full - 10:    
        mando.pos(scene, mando.x, mando.y + 1)

    mando.hitcheck(scene, coins, obs)

    print(scene.displayScene())


        
    for i in beams:  
        if(i.hit == 1):
            beams.remove(i)
            deletematrix(scene, i)
            del i
        elif(i.y < sc_full - 17):
            # i.hitcheck(scene)
            i.pos(scene, i.x, i.y + 3)
        else:
            beams.remove(i)
            deletematrix(scene, i)
            del i
    
    for i in dbeams:
        if(i.y > sc_full - sc_span - 10):
            # i.hitcheck(scene)
            i.pos(scene, i.x, i.y - 3)
        
        # elif(i and i.hit == 1):
        #     deletematrix(scene, i)
        #     # del i
        else:
            deletematrix(scene, i)
            del i

    for i in obs:
        
        if(i and i.hit == 1):
            deletematrix(scene, i)
            obs.remove(i)
            del i
        elif(i.y < sc_full - 4):
            i.hitcheck(scene, beams)
            if i.x < sc_top + 8:
                i.pos(scene, i.x, i.y)
        elif i.y <= scene.scenestart():
            obs.remove(i)
            del i
    
    for i in coins:
        if(i.hit == 1):
            coins.remove(i)
            deletematrix(scene, i)
            del i
        elif(i.y < sc_full - 4):
            i.pos(scene, i.x, i.y)
        elif i.y <= scene.scenestart():
            del i
    
    
    
    if  mando.getmagnet() == 1:
        mando.attract(magnet, scene)
        magnet.pos(scene, magnet.x, magnet.y + 1)
        elapsed = datetime.datetime.now() - start
        if scene.scenestart() >= sc_full - sc_span - 10 or elapsed.seconds > 10:
            deletematrix(scene, magnet)
            del magnet
            mando.unsetmagnet()
        