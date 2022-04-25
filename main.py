
import pygame as pg
from microbe import Microbe, create_world, add_food

n, m, a, leng = 60, 120, 10, 10
num_parents, popul, mut_speed, food = 5, 20, 20, 10

pg.init()
window = pg.display.set_mode((m*a, n*a))
clock = pg.time.Clock()

world = create_world(n, m, food)

microbes = []
for i in range(popul):
    microbes.append(Microbe(window, n, m, a, leng))
    x, y = microbes[-1].x, microbes[-1].y
    world[x][y] = 0


evolution, FPS, gener, sr_year = True, 30, 0, 0
while evolution:

    clock.tick(FPS)
    s = 'Эволюция' + ' '*10 \
        + '   Поколения: ' + str(gener) \
        + '   Длина жизни: ' + str(sr_year) \
        + '   Еда: ' + str(food) \
        + '   Мутации: ' + str(mut_speed)
    pg.display.set_caption(s)

    if FPS:
        window.fill((20, 90, 20))
        for i in range(n):
            for j in range(m):
                if world[i][j] == 1:
                    pg.draw.circle(window, (250, 0, 0), (j * a + a//2, i * a + a//2), a//4)
                if world[i][j] == 2:
                    pg.draw.circle(window, (0, 50, 0), (j * a + a//2, i * a + a//2), a//5)
                if world[i][j] == 3:
                    pg.draw.rect(window, (100, 100, 100), (j * a, i * a, a, a))

    keep = 0
    add_food(world, n, m, food)
    for mic in microbes:
        if mic.xp > 0:
            keep += 1
            mic.go(world)
            mic.set_xp(world)
            if FPS:
                mic.draw()

    if FPS:
        pg.display.flip()

    if keep <= num_parents:

        gener += 1
        world = create_world(n, m, food)
        sr_year = sum([m.year for m in microbes]) // len(microbes)

        # ОТБОР
        parents = sorted(microbes, reverse=True, key=lambda microbes: microbes.year)[:num_parents]

        # СЕЛЕКЦИЯ
        microbes = []
        for i in range(len(parents)):
            microbes += parents[i].selection(popul//num_parents)

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
                mut_speed += 1
            if e.key == pg.K_DOWN and mut_speed > 0:
                mut_speed -= 1
            if e.key == pg.K_g:
                print(microbes[0].genes)
