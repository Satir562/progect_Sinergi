# 0 - поле
# 1 - дерево
# 2 - река
# 3- госпиталь
# 4 - магозин улучьшений
# 5 - Огонь
import os

from utils import *
from clouds import *

CELL_TYPES = '🟩🌲🟦🏥🏪🔥'
TREE_BONUS = 100
#TODO увеличить на 5000
UPGRAD_COST = 500
LIVE_COST = 500
class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for _ in range(w)] for j in range(h)]

        self.generate_forest(3, 10)
        self.generate_rivers(50)
        self.generate_upgrade_shop()
        self.generate_hospital()
        self.clouds = Clouds(w,h)

    def check_bounds(self, x, y):
        if (x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True

    def print_map(self, helico):
        print('⬛' * (self.w + 2))
        for ri in range(self.h):
            print('⬛', end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (self.clouds.cells[ri][ci] == 1):
                    print("⛅", end='')
                elif (self.clouds.cells[ri][ci] == 2):
                    print("⚡", end="")

                elif (helico.x == ri and helico.y == ci):
                    print('🚁', end='')
                elif (cell >= 0 and cell <= len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end='')
            print('⬛')
        print('⬛' * (self.w + 2))

    def generate_rivers(self, l):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2
        while l > 0:
            rc2 = randcell2(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if (self.check_bounds(rx2, ry2)):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1

    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if rendbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generation_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.check_bounds(cx, cy) and self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1

    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy =c[0],c[1]
        self.cells[cx][cy]= 4

    def generate_hospital(self):
        c = randcell(self.w, self.h)
        cx, cy =c[0],c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy]= 3
        else:
            self.generate_hospital()

    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5

    def update_fire(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(5):
            self.add_fire()

    def process_helicopter(self, helico,clouds):
        c = self.cells[helico.x][helico.y]
        d = self.clouds.cells[helico.x][helico.y]
        if (c == 2):
            helico.tank = helico.mxtank
        if (c == 5 and helico.tank > 0):
            helico.tank -= 1
            helico.score += TREE_BONUS
            self.cells[helico.x][helico.y] = 1

        if (c == 4 and helico.score >= UPGRAD_COST):
            helico.mxtank += 1
            helico.score -= UPGRAD_COST
        if (c == 3 and helico.score >= LIVE_COST):
            helico.lives += 10
            helico.score -= LIVE_COST
        if (d == 2):
            helico.lives -= 1
            if (helico.lives == 0):

                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print('x         GAME OVER          x')
                print('x', "У ВАС ЗАКОНЧЕЛИСЬ ЖИЗНИ", helico.score, 'x')
                print('x                            x')
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                os.system('cls')
                exit(0)

    def export_date(self):
        return {'cells': self.cells}


    def import_date(self,date):
        self.cells = date['cells'] or [[0 for i in range(self.w)] for j in range(self.h)]
