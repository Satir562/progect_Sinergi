from game import clouds, helicopter
from map import Map
from helicopter import Helicopter as helico
from pynput import keyboard
from clouds import *
import time
import os
import json

TICK_SLEEP = 0.05
TREE_UPDAET = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 100
MAP_W, MAP_H =20,10
field = Map(MAP_W, MAP_H)

cloud = Clouds(MAP_W,MAP_H)
helico = helico(MAP_W,MAP_H)
tick = 1

MOVES = {'w': (-1,0), 'd': (0,1), 's': (1,0), 'a': (0,-1)}
# f -сохранение
# g - загрузка


def on_release(key):
    global helico, tick, cloud, field
    c = key.char.lower()
    if c in MOVES.keys():
        dx,dy =MOVES[c][0],MOVES[c][1]
        helico.move(dx,dy)
    elif c == 'f':
        date = {"helicopter": helico.export_data(),
                'clouds': cloud.export_date(),
                'field': field.export_date(),
                'tick': tick}
        with open('level.json', 'w') as lvl:
            json.dump(date, lvl)
    elif c == 'g':
        with open('level.json', 'r') as lvl:
            date = json.load(lvl)
            tick = date['tick'] or 1
            helico.import_date(date['helicopter'])
            field.import_date(date['field'])
            cloud.import_date(date['clouds'])

listener = keyboard.Listener(
    on_press=None,
    on_release=on_release)
listener.start()



while True:
    os.system('cls')

    field.process_helicopter(helico,clouds)
    helico.print_stats()
    field.print_map(helico)
    print("TICK", tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDAET == 0):
        field.generation_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fire()
    if (tick % CLOUDS_UPDATE == 0):
        field.clouds.update()