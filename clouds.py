from utils import rendbool


class Clouds:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]

    def update(self, r=1, mxr=20, g=1, mxg=10):
        for i in range(self.h):
            for j in range(self.w):
                if rendbool(r, mxr):
                    self.cells[i][j] = 1
                    if rendbool(g, mxg):
                        self.cells[i][j] = 2
                else:
                    self.cells[i][j] = 0



    def export_date(self):
        return  {'cells': self.cells}

    def import_date(self,date):
        self.cells = date['cells'] or [[0 for i in range(self.w)] for j in range(self.h)]
