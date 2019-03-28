from queue import Queue

INF = 10**6

class Point():
    x = y = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def up(self):
        return (self.x, self.y - 1)
    
    def right(self):
        return (self.x + 1, self.y)

    def down(self):
        return (self.x, self.y + 1)

    def left(self):
        return (self.x - 1, self.y)

    def neighbors(self):
        #up, left, right, down
        return [self.up(), self.left(), self.right(), self.down()]

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other or self.y != other.y


class Grid(list):
    def __getitem__(self, p):
        x, y = p.x, p.y
        return super.__getitem__(x, y)

def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_path(sx, sy, fx, fy, prev):
    cx, cy = fx, fy
    path = list()
    while (cx, cy) != (sx, sy):
        path.append((cx, cy))
        cx, cy = prev[cx][cy]
    path.append((cx, cy))
    path.reverse()
    return path


def a_star(sx, sy, fx, fy, n, m, grid):
    closed = []
    opened = []
    prev = [[None] * m for _ in range(n)]
    cur_dist = [[INF] * m for _ in range(n)]
    final_dist = [[INF] * m for _ in range(n)]

    opened.append((sx, sy))
    cur_dist[sx][sy] = 0
    final_dist[sx][sy] = heuristic(sx, sy, fx, fy)

    while len(opened):
        mini, cx, cy = INF, None, None
        for qx, qy in opened:
            if final_dist[qx][qy] < mini:
                mini = final_dist[qx][qy]
                cx, cy = qx, qy

        i = opened.index((cx, cy))
        del opened[i]
        

        for nx, ny in Point(cx, cy).neighbors():
            if not(0 <= nx <= m - 1) or not(0 <= ny <= n - 1):
                continue
            if (nx, ny) in closed:
                continue
            if grid[nx][ny] == '%':
                continue
            if (nx, ny) in opened:
                if cur_dist[cx][cy] + 1 < cur_dist[nx][ny]:
                    cur_dist[nx][ny] = cur_dist[cx][cy] + 1
                    final_dist[nx][ny] = cur_dist[nx][ny] + heuristic(nx, ny, fx, fy)    
                    prev[nx][ny] = (cx, cy)
            else:
                cur_dist[nx][ny] = cur_dist[cx][cy] + 1
                final_dist[nx][ny] = cur_dist[nx][ny] + heuristic(nx, ny, fx, fy)
                opened.append((nx, ny))
                prev[nx][ny] = (cx, cy)

        closed.append((cx, cy))
    return final_dist[fx][fy], get_path(sx, sy, fx, fy, prev)



FROMFILE = False
if FROMFILE:
    fin = open("input.txt")
    sx, sy = map(int, fin.readline().split())
    fx, fy = map(int, fin.readline().split())
    n, m = map(int, fin.readline().split())
    grid = [fin.readline().strip() for _ in range(n)]
else:
    sx, sy = map(int, input().split())
    fx, fy = map(int, input().split())
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

dist, path = a_star(sx, sx, fx, fy, n, m, grid)
print(dist)
for q in path:
    print(*q)