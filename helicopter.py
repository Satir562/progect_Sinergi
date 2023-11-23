from utils import randcell


class Helicopter:
    def __init__(self, w, h):
        rc = randcell(w, h)
        rx, ry = rc[0], rc[1]
        self.x = rx
        self.y = ry
        self.h = h
        self.w = w
        self.tank = 0
        self.mxtank = 1
        self.score = 0
        self.lives = 20

    def move(self, dx, dy):
        nx = dx + self.x
        ny = dy + self.y
        if (nx >= 0 and ny >= 0 and nx < self.h and ny < self.w):
            self.x, self.y = nx, ny

    def print_stats(self):
        print('💧 ', self.tank, '/', self.mxtank, sep='', end='|')
        print('🏆 ', self.score, end='|')
        print('❤ ', self.lives, end='|')

    def export_data(self):
        return {'score': self.score,
                'lives': self.lives,
                'x': self.x, 'y': self.y,
                'tank': self.tank,
                'mxtank': self.mxtank}

    def import_date(self, date):
        self.x = date['x'] or 0
        self.y = date['y'] or 0
        self.tank = date['tank'] or 0
        self.mxtank = date['mxtank'] or 1
        self.lives = date['lives'] or 3
        self.score = date['score'] or 0
