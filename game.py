import pygame as pg
import random as rnd
import copy

pg.init()

WIDTH = 500
HEIGHT = 550

screen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Py game")

fps = 60
timer = pg.time.Clock()

new_game = True

tubes = 10
colors = []
color_choices = ['red','blue','green','purple','light green','light blue','dark green','dark blue','orange','violet','pink','grey']

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

def draw_tubes(tubes_num, tubes_cols):
    tube_boxes = []
    if tubes % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True
    
    spacing = WIDTH / tubes_per_row

    for i in range(tubes_per_row):
        for j in range(len(tubes_cols[i])):
            pg.draw.rect(screen, color_choices[tubes_cols[i][j]], [5 + spacing*i, 200 - (50*j), 65, 50], 0, 3)
        box = pg.draw.rect(screen, 'white', [5 + spacing*i, 50, 65, 200], 5, 3)
        tube_boxes.append(box)

    return tube_boxes

run = True
while run:
    screen.fill("black")
    timer.tick(fps)

    if new_game:
        tubes, colors = generate_start()
        initial_colors = copy.deepcopy(colors)
        new_game = False
    else:
        tube_rects = draw_tubes(tubes, colors)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()
pg.quit()