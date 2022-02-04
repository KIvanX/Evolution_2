import pygame as pg
from microbe import Microbe, create_world

n, m, a, l = 60, 120, 10, 5
live, num_parents, popul, mut_speed, food = 100, 10, 30, 20, 10

pg.init()
window = pg.display.set_mode((m*a, n*a))
clock = pg.time.Clock()

world = create_world(n, m, food)

microbes = []
for i in range(popul):
    microbes.append(Microbe(window, n, m, a, l))
    x, y = microbes[-1].x, microbes[-1].y
    world[x][y] = 0


evolution, FPS, year, gener, sr_score = True, 300, 0, 0, 0
while evolution:
    clock.tick(FPS)
    s = 'Эволюция' + ' '*10 \
        + '   Поколения: ' + str(gener) \
        + '   Очки: ' + str(sr_score) \
        + '   Жизнь: ' + str(live) \
        + '   Еда: ' + str(food) \
        + '   Мутации: ' + str(mut_speed)
    pg.display.set_caption(s)

    if FPS:
        window.fill((20, 50, 20))
        for i in range(n):
            for j in range(m):
                if world[i][j] == 1:
                    pg.draw.circle(window, (250, 0, 0), (j * a + a//2, i * a + a//2), a//4)
                if world[i][j] == 2:
                    pg.draw.circle(window, (20, 80, 20), (j * a + a//2, i * a + a//2), a//5)
                if world[i][j] == 3:
                    pg.draw.rect(window, (100, 100, 100), (j * a, i * a, a, a))
        pg.display.flip()

    for mic in microbes:
        mic.go(world)
        mic.set_score(world)
        if FPS:
            mic.draw()

    year += 1
    if year >= live:
        year = 0
        gener += 1
        world = create_world(n, m, food)
        sr_score = sum([m.score for m in microbes]) // len(microbes)

        # ОТБОР
        parents = sorted(microbes, reverse=True, key=lambda microbes: microbes.score)[:num_parents]

        # СЕЛЕКЦИЯ
        microbes = []
        for i in range(len(parents) // 2):
            microbes += parents[i].selection(parents[len(parents)-i-1], popul//num_parents)

        # МУТАЦИЯ
        for mic in microbes:
            mic.mutation(mut_speed)

        # print(*microbes[0].genes)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            evolution = False

        if e.type == pg.KEYUP:
            if e.key == pg.K_SPACE:
                FPS = 30 if FPS == 0 else 0
            if e.key == pg.K_LEFT and food > 0:
                food -= 1
            if e.key == pg.K_RIGHT:
                food += 1
            if e.key == pg.K_UP:
                live += 10
            if e.key == pg.K_DOWN and live > 10:
                live -= 10
            if e.key == pg.K_KP8:
                mut_speed += 1
            if e.key == pg.K_KP2 and mut_speed >= 0:
                mut_speed -= 1
            if e.key == pg.K_g:
                print(*microbes[0].genes)
