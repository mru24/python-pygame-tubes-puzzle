import pygame as pg
import random as rnd
import copy
import time

pg.init()

col_number = 4

WIDTH = 320
HEIGHT = 660

screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
pg.display.set_caption("Py game")

fps = 60
timer = pg.time.Clock()

font = pg.font.Font('freesansbold.ttf', 16)
fontLG = pg.font.Font('freesansbold.ttf', 46)

new_game = True

tubes = 20

tile_height = 50
min_tubes = 5
max_tubes = 7
level = 1
colors = []
initial_colors = []
color_choices = [
    'red',
    'blue',
    'green',
    'purple',
    'orange',
    'violet',
    'grey',
    'light blue',
    'dark green',
    'dark blue',
    'pink',
    'light green',
    'antiquewhite',
    'aqua',
    'brown',
    'burlywood1'
    ]

selected = False
tube_rects = []
select_rect = 100

win = False

def generate_start():
    tubes_number = rnd.randint(min_tubes, max_tubes)
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(col_number):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(col_number):
            color = rnd.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    # print(tubes_colors, tubes_number)
    return tubes_number, tubes_colors


def draw_tubes(tubes_num, tubes_cols):
    tube_boxes = []
    if tubes % 2 == 0:
        tubes_per_row = tubes_num // 2
        offset = False
    else:
        tubes_per_row = tubes_num // 2 + 1
        offset = True
    
    

    tile_width = (WIDTH / tubes_per_row)-15
    spacing = tile_width+10

    for i in range(tubes_per_row):
        for j in range(len(tubes_cols[i])):
            pg.draw.rect(screen, color_choices[tubes_cols[i][j]], [15 + spacing*i, (col_number*tile_height)-(tile_height*j)+30, tile_width, tile_height], 0, 5)
        box = pg.draw.rect(screen, 'white', [15 + spacing*i, 80, tile_width, (col_number*tile_height)], 2, 5)
        if select_rect == i:
            pg.draw.rect(screen, 'red', [15 + spacing * i, 80, tile_width, (col_number*tile_height)], 4, 5)
        tube_boxes.append(box)

    if offset:
        for i in range(tubes_per_row - 1):
            for j in range(len(tubes_cols[i + tubes_per_row])):
                pg.draw.rect(screen, color_choices[tubes_cols[i + tubes_per_row][j]], [15 + (spacing * 0.5) + spacing*i, (col_number*tile_height*2)-(50*j)+40, tile_width, tile_height], 0, 5)            
            box = pg.draw.rect(screen, 'white', [15 + (spacing * 0.5) + spacing * i, (col_number*tile_height+90), tile_width, (col_number*tile_height)], 2, 5)
            if select_rect == i + tubes_per_row:
                pg.draw.rect(screen, 'red', [15 + (spacing * 0.5) + spacing * i, (col_number*tile_height+90), tile_width, (col_number*tile_height)], 4, 5)
            tube_boxes.append(box)    
    else:
        for i in range(tubes_per_row):
            for j in range(len(tubes_cols[i + tubes_per_row])):
                pg.draw.rect(screen, color_choices[tubes_cols[i + tubes_per_row][j]], [15 + spacing*i, (col_number*tile_height*2)-(50*j)+40, tile_width, tile_height], 0, 0)
            box = pg.draw.rect(screen, 'white', [15 + spacing*i, (col_number*tile_height+90), tile_width, (col_number*tile_height)], 2, 5)
            if select_rect == i + tubes_per_row:
                pg.draw.rect(screen, 'red', [15 + spacing * i, (col_number*tile_height+90), tile_width, (col_number*tile_height)], 2, 5)
            tube_boxes.append(box)
    return tube_boxes

def calc_move(colors, selected_rect, destination):
    chain = True
    length = 1
    color_on_top = 100
    color_to_move = 100
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[select_rect][-1]
        for i in range(1,len(colors[select_rect])):
            if chain:
                if colors[select_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if col_number > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        for i in range(length):
            if len(colors[destination]) < col_number:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
    return colors

def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != col_number:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won

def level_up(level,min_tubes,max_tubes):
    level += 1
    if level % 3 == 0:
        min_tubes += 1
        max_tubes += 1
    return level,min_tubes,max_tubes

def add_tube(num,level):
    if level % 6 == 0:
        num += 1
    return num

run = True

while run:
    screen.fill("black")
    timer.tick(fps)

    if new_game:
        col_number = add_tube(col_number,level)
        tubes, colors = generate_start()
        initial_colors = copy.deepcopy(colors)
        new_game = False
        if win:
            level,min_tubes,max_tubes = level_up(level,min_tubes,max_tubes)            
            print(col_number)
    else:
        tube_rects = draw_tubes(tubes, colors)
    win = check_victory(colors)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                colors = copy.deepcopy(initial_colors)
            elif event.key == pg.K_RETURN:
                new_game = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        colors = calc_move(colors, select_rect, dest_rect)
                        selected = False
                        select_rect = 100

    if win:
        victory_text = fontLG.render('You Win!', True, 'gold')
        screen.blit(victory_text, (70, HEIGHT/2-20))

    level_text = font.render(('Level: %d' % level), True,'lightgrey')
    screen.blit(level_text,(10,10))
    restart_text = font.render('Stuck? Space - Restart', True, 'white')
    screen.blit(restart_text,(10, 30))
    restart_text = font.render('Enter - New Board!', True, 'white')
    screen.blit(restart_text,(10, 50))

    pg.display.flip()

    if win:
        pg.time.delay(3000)
        new_game = True

pg.quit()