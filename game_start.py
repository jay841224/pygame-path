import pygame, sys
import numpy as np
from math import sqrt
pygame.init()

def define_block():#distriction of drawing
    ox = []
    oy = []
    while True:
        draw = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                draw = True
                if mouse[0] < button_width*4 and mouse[0] > button_width*3 and mouse[1] < 40 and mouse[1] > 0:
                    draw_block_but.change_color(white)
                    draw_block_but.draw(background, black)
                    return ox, oy
            while draw:
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        draw = False
                if mouse[1] > 40:
                    x = mouse[0]//4
                    y = mouse[1]//4
                    if ox == []:
                        ox.append(x)
                        oy.append(y)
                    if ox != []:
                        if ox[-1] != x or oy[-1] != y:
                            ox.append(x)
                            oy.append(y)
                    pygame.draw.rect(background, [255, 0, 0], ((4*x, 4*y), (4, 4)))
                    print(pygame.Rect(((4*x, 4*y), (4, 4))))
                    screen.blit(background, (0, 0))
                    pygame.display.update()
                


def start_window(size):
    screen = pygame.display.set_mode(size)
    background = pygame.display.set_mode(size)
    return screen, background

def define_a_pos_st(ox, oy):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
            
                if mouse[0] < button_width*4 and mouse[0] > button_width*3 and mouse[1] < 40 and mouse[1] > 0:
                        draw_block_but.change_color(white)
                        draw_block_but.draw(background, black)
                        choose_start_but.change_color(white)
                        choose_start_but.draw(background, black)
                        return x, y
                else:
                    x = mouse[0]//4
                    y = mouse[1]//4
                    try:
                        pygame.draw.rect(background, [25, 80, 50], ((old_x*4, old_y*4), (4, 4)))
                        pygame.draw.rect(background, black, ((old_x*4, old_y*4), (4, 4)), 1)
                    except:
                        pass
                    if y > 10:
                        if not (x, y) in zip(ox, oy):
                            pygame.draw.rect(background, yellow, ((x*4, y*4), (4, 4)))
                    old_x = x
                    old_y = y
        pygame.display.update()
def define_a_pos_end(ox, oy):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
            
                if mouse[0] < button_width*4 and mouse[0] > button_width*3 and mouse[1] < 40 and mouse[1] > 0:
                        draw_block_but.change_color(white)
                        draw_block_but.draw(background, black)
                        choose_end_but.change_color(blue)
                        choose_end_but.draw(background, white)
                        return x, y
                else:
                    x = mouse[0]//4
                    y = mouse[1]//4
                    try:
                        pygame.draw.rect(background, [25, 80, 50], ((old_x*4, old_y*4), (4, 4)))
                        pygame.draw.rect(background, black, ((old_x*4, old_y*4), (4, 4)), 1)
                    except:
                        pass
                    if y > 10:
                        if not (x, y) in zip(ox, oy):
                            pygame.draw.rect(background, red, ((x*4, y*4), (4, 4)))
                    old_x = x
                    old_y = y
        pygame.display.update()

def draw_rect(x, y, color):
    pygame.draw.rect(background, color, ((x*4 + 1, (y + 10)*4 + 1), (2, 2)))
    pygame.display.update()
class button():
    def __init__(self, color, x, y, width, heigh, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.heigh = heigh
        self.color = color
        self.text = text
    
    def draw(self, win, color, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.heigh+4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.heigh), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, color)
            win.blit(text, (self.x + self.width/2 - text.get_width()/2, self.y + (self.heigh/2 - text.get_height()/2)))
        pygame.display.update()

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.width:
                return True
        return False

    def change_color(self, color):
        self.color = color

class Dijkstra:
    def __init__(self, ox, oy):
        self.ox = ox
        self.oy = oy
        self.motion = self.get_motion()
        self.block = self.get_block()

    class Node:
        def __init__(self, x, y, cost, pind):
            self.x = x
            self.y = y
            self.cost = cost
            self.pind = pind


    def planning(self, sx, sy, gx, gy):
        start_point = self.Node(sx, sy, 0, -1)
        goal_point = self.Node(gx, gy, 0, -1)

        openset, closeset = {}, {}
        openset[self.cal_index(start_point)] = start_point

        while True:
            c_id = min(openset, key=lambda o:openset[o].cost)
            current = openset[c_id]
            closeset[c_id] = current#add the past point
            del openset[c_id]
            draw_rect(current.x, current.y, blue)

            if c_id == self.cal_index(goal_point):
                goal_point.cost = current.cost
                goal_point.pind = current.pind
                break

            for i, _ in enumerate(self.motion):
                node = self.Node(current.x + self.motion[i][0],
                                current.y + self.motion[i][1],
                                current.cost + self.motion[i][2],
                                c_id)
                n_id = self.cal_index(node)
                if n_id in closeset:
                    continue
                if not self.verify_node(node):
                    continue
                if not n_id in openset:
                    openset[n_id] = node
                else:
                    if openset[n_id].cost > node.cost:
                        openset[n_id] = node
        rx, ry = self.cal_final_path(goal_point, closeset)
        return rx, ry

    def cal_final_path(self, goal_point, closeset):
        rx = [goal_point.x]
        ry = [goal_point.y]
        pind = goal_point.pind
        while pind != -1:
            rx.append(closeset[pind].x)
            ry.append(closeset[pind].y)
            pind = closeset[pind].pind

        return rx, ry



    def verify_node(self, node):
        if node.x >= x_dir_box or node.x <= 0 or node.y >= x_dir_box or node.y <= 0:
            return False
        if self.block[node.x][node.y]:
            return False
        return True


    def get_block(self):
        block = [[False for _ in range(x_dir_box)] for _ in range(x_dir_box)]

        for x in range(x_dir_box):
            for y in range(x_dir_box):
                for bx, by in zip(self.ox, self.oy):
                    if sqrt((bx - x)**2 + (by - y)**2) < 0.1:
                        block[x][y] = True
        return block
    
    def get_motion(self):
        motion = [
            [1, 0, 1],
            [0, 1, 1],
            [-1, 0, 1],
            [0, -1, 1]
            #[1, 1, sqrt(2)],
            #[1, -1, sqrt(2)],
            #[-1, 1, sqrt(2)],
            #[-1, -1, sqrt(2)]
        ]
        return motion



    
    def cal_index(self, p):
        return p.x + p.y*x_dir_box

x_dir_box = 150

screen, background = start_window((600, 440))
white = [255, 255, 255]
blue = [0, 0, 150]
black = [0, 0, 0]
yellow = [255, 255, 0]
red = [255, 0, 0]
button_width = 80
#window set button
choose_start_but = button(white, 0, 0, button_width, 40, text='choose start')
choose_start_but.draw(background, black)
choose_end_but = button(blue, button_width, 0, button_width, 40, text='choose end')
choose_end_but.draw(background, white)
draw_block_but = button(white, button_width*2, 0, button_width, 40, text='draw block')
draw_block_but.draw(background, black)
draw_ok_but = button(blue, button_width*3, 0, button_width, 40, text='ok')
draw_ok_but.draw(background, white)
draw_go_button = button(white, button_width*4, 0, button_width, 40, text='go')
draw_go_button.draw(background, black)
draw_restart_but = button(blue, button_width*5, 0, button_width, 40, text='restart')
draw_restart_but.draw(background, white)

for row in range(x_dir_box):
    for col in range(10, 110):
        pygame.draw.rect(background, [25, 80, 50], ((row*4, col*4), (4, 4)))
        pygame.draw.rect(background, [0, 0, 0], ((row*4, col*4), (4, 4)), 1)

screen.blit(background, (0, 0))
pygame.display.update()



oxx = []
oyy = []
sx = None
sy = None
ex = None
ey = None
run = True
while run:
    block = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] < button_width and mouse[0] > 0 and mouse[1] < 40 and mouse[1] > 0:#define start
                sx = None
                sy = None
                choose_start_but.change_color(yellow)
                choose_start_but.draw(background, black)
                sx, sy = define_a_pos_st(oxx, oyy)
            if mouse[0] < button_width*2 and mouse[0] > button_width and mouse[1] < 40 and mouse[1] > 0:#define end
                ex = None
                ey = None
                choose_end_but.change_color(yellow)
                choose_end_but.draw(background, white)
                ex, ey = define_a_pos_end(oxx, oyy)
            if mouse[0] < button_width*3 and mouse[0] > button_width*2 and mouse[1] < 40 and mouse[1] > 0:#draw block
                draw_block_but.change_color(yellow)
                draw_block_but.draw(background, black)
                block = True
            while block:
                ox, oy = define_block()
                oxx += ox
                oyy += oy
                block = False

            if mouse[0] < button_width*5 and mouse[0] > button_width*4 and mouse[1] < 40 and mouse[1] > 0:
                dijkstra = Dijkstra(oxx, [oy - 10 for oy in oyy])
                rx, ry = dijkstra.planning(sx, sy - 10, ex, ey - 10)
                for x, y in zip(rx, ry):
                    draw_rect(x, y, yellow)
                pygame.draw.rect(background, yellow, ((sx*4, sy*4), (4, 4)))
                pygame.draw.rect(background, red, ((ex*4, ey*4), (4, 4)))

            if mouse[0] < button_width*6 and mouse[0] > button_width*5 and mouse[1] < 40 and mouse[1] > 0:
                oxx = []
                oyy = []
                sx = None
                sy = None
                ex = None
                ey = None
                for row in range(x_dir_box):
                    for col in range(10, 110):
                        pygame.draw.rect(background, [25, 80, 50], ((row*4, col*4), (4, 4)))
                        pygame.draw.rect(background, [0, 0, 0], ((row*4, col*4), (4, 4)), 1)

        if event.type == pygame.QUIT:
            pygame.quit()
    try:
        pygame.display.update()

    except:
        run = False