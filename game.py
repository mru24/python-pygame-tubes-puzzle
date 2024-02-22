import pygame as pg
import random as rnd

pg.init()

WIDTH = 500
HEIGHT = 500

screen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Py game")

fps = 60
timer = pg.time.Clock()

new_game = True

tubes = 10
colors = []

def generate_start():
    tubes_number = rnd.randint(10, 14)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = rnd.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    print(tubes_colors, tubes_number)
    return tubes_number, tubes_colors

run = True
while run:
    screen.fill("black")
    timer.tick(fps)

    if new_game:
        tubes, colors = generate_start()
        new_game = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()
pg.quit()