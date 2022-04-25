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


def add_food(world, n, m, food):
    for i in range(food // 5):
        world[randint(0, n-1)][randint(0, m-1)] = 1
    return world


class Microbe:
    def __init__(self, window, n, m, a, leng):
        self.genes = [random()-0.5 for _ in range(3*leng)]
        # self.genes = [102.4, 51.2, 25.6, 12.8, 6.4, 3.2, 1.6, 0.8, 0.4, 0.2, 0.1, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.xp, self.year = 30, 0
        self.n, self.m, self.a, self.leng = n, m, a, leng
        self.x, self.y = randint(0, n-1), randint(0, m-1)
        self.window, self.font = window, pg.font.SysFont('arial', 10)
        self.way = (0, 0)

    def draw(self):
        r = self.a // 2
        pg.draw.circle(self.window, (250, 250, 0), (self.y*self.a + r, self.x*self.a + r), int(r*0.8))
        # render = self.font.render(str(self.score), True, (0, 0, 0))
        # self.window.blit(render, (self.y*self.a + r//2, self.x*self.a + r//2))

    def go(self, world):
        objs = []
        for i in range(max(0, self.x - self.leng), min(self.n, self.x + self.leng)):
            for j in range(max(0, self.y - self.leng), min(self.m, self.y + self.leng)):
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
                if dist[i] == min(dist) or dist[i] == min(dist)-1:
                    att[i] += self.genes[(obj[2] - 1) * self.leng + dist[i]]

        good_ways = []
        for i in range(len(att)):
            if abs(att[i] - max(att)) < 0.1:
                if 0 <= self.x + ways[i][0] < self.n and 0 <= self.y + ways[i][1] < self.m:
                    if world[self.x + ways[i][0]][self.y + ways[i][1]] != 3:
                        good_ways.append(ways[i])

        if len(good_ways) > 0:
            if not(self.way in good_ways):
                self.way = choice(good_ways)

            self.x += self.way[0]
            self.y += self.way[1]

    def set_xp(self, world):
        if world[self.x][self.y] == 1:
            world[self.x][self.y] = 0
            self.xp += 5
        if world[self.x][self.y] == 2:
            world[self.x][self.y] = 0
            self.xp -= 30

        if self.xp > 0:
            self.year += 1
        self.xp -= 1

        self.xp = 0 if self.xp < 0 else self.xp
        self.xp = 100 if self.xp > 100 else self.xp

    def selection(self, num_children):
        children = []
        for i in range(num_children):
            child = Microbe(self.window, self.n, self.m, self.a, self.leng)

            for i in range(len(self.genes)):
                child.genes[i] = self.genes[i]

            children.append(child)

        return children

    def mutation(self, speed):
        if speed > 0:
            for i in range(len(self.genes)):
                self.genes[i] += (random() - 0.5) / (100 // speed)
