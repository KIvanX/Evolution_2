import pygame as pg
from random import random, randint, choice


def create_world(n, m, food):
    a = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            if not randint(0, 100//food):
                a[i][j] = 1
            if not randint(0, 30):
                a[i][j] = 2
            # if not randint(0, 300):
            #     i1 = i
            #     while i1 < n and randint(0, 10):
            #         a[i1][j] = 3
            #         i1 += 1

    return a


class Microbe:
    def __init__(self, window, n, m, a, l):
        self.genes = [random()-0.5 for _ in range(3*l)]
        self.score = 0
        self.n, self.m, self.a, self.l = n, m, a, l
        self.x, self.y = randint(0, n-1), randint(0, m-1)
        self.window, self.font = window, pg.font.SysFont('arial', 10)
        self.way = (1, 1)

    def draw(self):
        r = self.a // 2
        pg.draw.circle(self.window, (250, 250, 0), (self.y*self.a + r, self.x*self.a + r), int(r*0.8))
        # render = self.font.render(str(self.score), True, (0, 0, 0))
        # self.window.blit(render, (self.y*self.a + r//2, self.x*self.a + r//2))
        pg.display.flip()

    def go(self, world):
        objs = []
        for i in range(max(0, self.x - self.l), min(self.n, self.x + self.l)):
            for j in range(max(0, self.y - self.l), min(self.m, self.y + self.l)):
                if world[i][j] != 0:
                    objs.append([i - self.x, j - self.y, world[i][j]])

        att = [0] * 8
        ways = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for obj in objs:
            dist = []
            for i in range(len(ways)):
                sx, sy = abs(obj[0] - ways[i][0]), abs(obj[1] - ways[i][1])
                dist.append(min(sx, sy) + abs(sx - sy))

            for i in range(len(dist)):
                if dist[i] == min(dist):
                    att[i] += self.genes[(obj[2] - 1) * self.l + dist[i]]

        good_ways = []
        for i in range(len(att)):
            if abs(att[i] - max(att)) < 0.1:
                if 0 <= self.x + ways[i][0] < self.n and 0 <= self.y + ways[i][1] < self.m:
                    if world[self.x + ways[i][0]][self.y + ways[i][1]] != 3:
                        good_ways.append(ways[i])

        if len(good_ways) > 0:
            if not(self.way in good_ways and randint(0, 2)):
                self.way = choice(good_ways)

            self.x += self.way[0]
            self.y += self.way[1]

    def set_score(self, world):
        if world[self.x][self.y] == 1:
            world[self.x][self.y] = 0
            self.score += 1
        if world[self.x][self.y] == 2:
            world[self.x][self.y] = 0
            self.score -= 3
        self.score -= 0.01

    def selection(self, microbe, num_children):
        children = []
        for i in range(num_children):
            child = Microbe(self.window, self.n, self.m, self.a, self.l)

            for i in range(len(self.genes)):
                child.genes[i] = (self.genes[i] + microbe.genes[i]) / 2

            children.append(child)

        return children

    def mutation(self, speed):
        if speed > 0:
            for i in range(len(self.genes)):
                self.genes[i] += (random() - 0.5) / (100 // speed)
