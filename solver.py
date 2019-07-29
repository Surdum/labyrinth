import copy
from time import sleep, time
from PIL import Image, ImageDraw
# from labgen import *
# import labirinth_generator


matrix = [
    ['0', '0', '#', 'A', '#', '#', '#', '#', '#', '0', '#', '0', '#', '#', '#', '#'],
    ['#', '0', '0', '0', '#', '0', '0', '0', '#', '0', '0', '0', '#', '0', '0', '0'],
    ['0', '0', '#', '#', '#', '0', '#', '0', '0', '0', '#', '#', '#', '0', '#', '0'],
    ['#', '0', '#', '0', '0', '0', '#', '0', '#', '0', '#', '0', '0', '0', '#', '0'],
    ['0', '0', '0', '0', '#', '#', '#', '0', '0', '0', '0', '0', '#', '#', '#', '0'],
    ['0', '0', '#', '#', '#', '#', '#', '#', '#', '0', '#', '0', '#', '#', '#', '#'],
    ['#', '0', '0', '0', '#', '0', '0', '0', '#', '0', '0', '0', '#', '0', '0', '0'],
    ['0', '0', '#', '#', '#', '0', '#', '0', '0', '0', '#', '#', '#', '0', '#', '0'],
    ['#', '0', '#', '0', '0', '0', '#', '0', '#', '#', '#', '0', '0', '0', '#', '0'],
    ['0', '0', '0', '0', '#', '#', '#', '0', '0', '0', '0', '0', '#', '#', '#', '0'],
    ['#', '#', '#', '0', '#', '0', '0', '0', '#', '#', '#', '0', '#', '0', '0', 'B']]
"""
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == '#':
            matrix[i][j] = 0
        elif matrix[i][j] == '0':
            matrix[i][j] = 1
        elif matrix[i][j] == 'A':
            matrix[i][j] = 2
        elif matrix[i][j] == 'B':
            matrix[i][j] = 3
"""
# for line in matrix:
#     print(line)

def get_round_points(pnt, m):
    points = []
    t = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for pare in t:
        i = pnt[0] + pare[0]
        j = pnt[1] + pare[1]
        if len(m) > i >= 0 and len(m[0]) > j >= 0 and m[i][j] in '01B':
            points.append((i, j))

#    for i in range(pnt[0] - 1, pnt[0] + 2, 1):
#        for j in range(pnt[1] - 1, pnt[1] + 2, 1):
#            if len(m) > i >= 0 and len(m[0]) > j >= 0 and m[i][j] in '01B':
#                points.append((i, j))
    return points


def dijkstra(matrix):
    # m = matrix.copy()
    m = copy.deepcopy(matrix)

    m = list(map(lambda line: list(map(lambda x: str(x), line)), m))
    m1 = copy.deepcopy(m)
    ind = sum(m, []).index('A')
    # print(ind)

    i = ind // len(m[0])
    j = ind % len(m[0])

    paths = [[(i, j)]]
    # print(paths)
    end = False
    new_paths = []
    st = time()
    while not end:
        for path in paths:
            points = get_round_points(path[-1], m)
            if not points:
                continue
            for point in points:
                if m[path[-1][0]][path[-1][1]] != 'A':
                    m[path[-1][0]][path[-1][1]] = '2'
                    if m[point[0]][point[1]] == 'B':
                        print('Total', time() - st)
                        end = True
                        print(path)
                        print(len(path))
                        for i, elem in enumerate(path[1:]):
                            m1[elem[0]][elem[1]] = '.'

                        break

                new_paths.append(path + [point])
                m[point[0]][point[1]] = '1'
            # если найдены пути, взять первый из них
            if end:
                break
        paths = new_paths
        new_paths = []
    return m1


def greedy_bfs(matrix):
    m = copy.deepcopy(matrix)
    return m


def astar(matrix):
    m = copy.deepcopy(matrix)
    return m


def view(name, m):
    print(name)
    print('_' * 3 * len(m[0]))
    for elem in m:
        print('[ ' + ' '.join(list(map(lambda x: str(x).replace('0', ' '), elem))))
    print()


def open_lab(name, n):
    pic = Image.open(name)
    w, h = pic.size
    pix = pic.load()
    lab = []
    # print(pix[1, 1])
    for y in range(0, h, n):
        line = []
        for x in range(0, w, n):
            p = pix[y, x]
            line.append('#' if p == (0, 0, 0) else '0' if p == (255, 255, 255) else 'A' if p == (0, 255, 0) else 'B' if p == (0, 0, 255) else '')
        lab.append(line)
    return lab


def draw_lab(lab, name, n):
    w, h = len(lab), len(lab[0])
    pic = Image.new('RGB', (w*n, h*n))
    draw = ImageDraw.Draw(pic)
    for x in range(w):
        for y in range(h):
            p = ()
            if lab[x][y] == '#':
                p = (0, 0, 0)
            elif lab[x][y] == '.':
                p = (255, 0, 0)
            elif lab[x][y] == '0':
                p = (255, 255, 255)
            elif lab[x][y] == 'A':
                # print('A', x, y)
                p = (0, 255, 0)
            elif lab[x][y] == 'B':
                p = (0, 0, 255)
                # print('B', x, y)
            # draw.point((x, y), p)
            draw.rectangle([(x*n, y*n), (x*n+n, y*n+n)], p)
    pic.save(name)


if __name__ == '__main__':
    """
    m1 = diikstra(matrix)
    m2 = greedy_bfs(matrix)
    m3 = astar(matrix)
    
    view('Оригинал', matrix)
    view('Дийкстра', m1)
    view('Best first search', m2)
    view('А*', m3)
    """

    m = open_lab('lab500x500.png', 2)

    m = dijkstra(m)

    draw_lab(m, 'lab500x500_solved.png', 2)


