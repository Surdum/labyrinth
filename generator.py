from PIL import Image, ImageDraw
from random import choice, seed
from time import time


# seed(666)


class Labyrinth:
    def __init__(self, size):
        if size[0] % 2 == 0:
            size[0] += 1
        if size[1] % 2 == 0:
            size[1] += 1

        self.w, self.h = size
        self.paths = []
        self.visited = []
        self.len = 0
        self.endpoint = ()
        self.breakpoints = []
        self.current_point = ()
        self.labyrinth = [[0 for _ in range(size[1])] for __ in range(size[0])]
        self.__empty = self.labyrinth.copy()
        for i in range(self.w):
            for j in range(self.h):
                if i % 2 == 1 and j % 2 == 1:
                    self.labyrinth[i][j] = 1

    def load(self, name, n):
        pic = Image.open(name)
        w, h = pic.size
        pix = pic.load()
        for x in range(0, w, n):
            for y in range(0, h, n):
                if pix[y, x] == (133, 133, 133):
                    self.visited.append((y, x))
                    self.len += 1
                elif pix[y, x] == (133, 133, 0):
                    self.endpoint = (y, x)

    def __get_points(self, p):
        points = []
        if (p[0] + 2, p[1]) not in self.visited and p[0] + 2 < self.w:
            points.append((p[0] + 2, p[1]))
        if (p[0], p[1] + 2) not in self.visited and p[1] + 2 < self.h:
            points.append((p[0], p[1] + 2))
        if (p[0] - 2, p[1]) not in self.visited and p[0] - 2 > 0:
            points.append((p[0] - 2, p[1]))
        if (p[0], p[1] - 2) not in self.visited and p[1] - 2 > 0:
            points.append((p[0], p[1] - 2))
        return points

    def __find_way(self, start):
        f = True
        path = [start]
        self.current_point = start
        while f:
            points = self.__get_points(self.current_point)
            if not points:
                f = False
            else:
                point = choice(points)
                if point == self.endpoint:
                    self.visited = self.visited[self.len:]
                    # print('deleted')
                self.labyrinth[(self.current_point[0] + point[0]) // 2][(self.current_point[1] + point[1]) // 2] = 1
                self.current_point = point
                self.visited.append(point)
                path.append(point)

        self.paths.append(path)
        self.breakpoints.append([len(self.paths) - 1, len(path) - 1])

    def __back_search(self):
        while True:
            if len(self.breakpoints) == 0:
                return None
            path, i = self.breakpoints[-1]
            while i >= 0:
                points = self.__get_points(self.paths[path][i])
                if points:
                    self.breakpoints[-1] = [path, i]
                    return self.paths[path][i]
                i -= 1
            if i <= 0:
                del self.breakpoints[-1]

    def generate_labyrinth(self, start=(1, 1)):
        self.visited.append(start)
        point = start
        while True:
            self.__find_way(point)
            point = self.__back_search()
            if point is None:
                break
            # self.labyrinth[point[0]][point[1]] = 123

    def draw_labyrinth(self, name, n=10, lab=None):
        if lab is None:
            lab = self.labyrinth

        pic = Image.new('RGB', (self.w * n, self.h * n))
        draw = ImageDraw.Draw(pic)
        for i in range(self.w):
            for j in range(self.h):
                if lab[i][j] == 0:
                    draw.rectangle([(i * n, j * n), (i * n + n, j * n + n)], fill=(0, 0, 0))
                elif lab[i][j] == 2:
                    draw.rectangle([(i * n, j * n), (i * n + n, j * n + n)], fill=(0, 255, 0))
                elif self.labyrinth[i][j] == 666:
                    draw.rectangle([(i * n, j * n), (i * n + n, j * n + n)], fill=(255, 0, 0))
                elif lab[i][j] == 3:
                    draw.rectangle([(i * n, j * n), (i * n + n, j * n + n)], fill=(0, 0, 255))
                else:
                    draw.rectangle([(i * n, j * n), (i * n + n, j * n + n)], fill=(255, 255, 255))
        pic.save(f'{name}.png')

    def print(self):
        for line in self.labyrinth:
            print(line)

    def add_start_end(self, start, end):
        self.labyrinth[start[0]][start[1]] = 2
        self.labyrinth[end[0]][end[1]] = 3


if __name__ == '__main__':
    st = time()
    s = [15, 15]
    lab = Labyrinth(s)
    # lab.load('lab9x9_patt.png', 1)
    lab.generate_labyrinth()
    lab.add_start_end((1, 1), (s[0] - 2, s[1] - 2))
    lab.draw_labyrinth(f'lab15x15', 10)

    print('Total', time() - st)
