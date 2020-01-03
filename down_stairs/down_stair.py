import pygame
import numpy as np
import random, time
from pygame.locals import *

pygame.init()
win = pygame.display.set_mode((800, 800), 0, 32)
win2 = pygame.Surface(600, 800)
clock = pygame.time.Clock()

#color set
black = [0, 0, 0]
blue = [0, 0, 255]
red = [255, 0, 0]
white = [255, 255, 255]

bar_class = [blue, red, white]
right_surface = pygame.Surface((200, 800))#新的surface 位於右邊記分板
right_surface.fill([0, 58, 0])



class people:
    def __init__(self):
        self.raw_image = pygame.image.load(r'./pic/face.png').convert_alpha()
        self.img = pygame.transform.scale(self.raw_image, (30, 30))
        self.pos = [400, 100]

    def move(self, direct):
        
        if direct[0]:
            self.pos[0] -= 3
        if direct[1]:
            self.pos[0] += 3
        #win.fill(black)
        win.blit(self.img, self.pos)

    def drop_down(self):
        self.pos[1] += 1
        #win.fill(black)
        win.blit(self.img, self.pos)
        if self.pos[1] > 800:
            return False
        return True

    def is_collapse(self, bar_list):
        for x in bar_list:
            #print(x.rect[1] - self.pos[1])
            if self.pos[0] - x.ran_pos[0] < x.size[0]  and self.pos[0] - x.ran_pos[0] >=-30 and  x.rect[1] - self.pos[1] - 30 > -5 and x.rect[1] - self.pos[1] - 30 <= 5:
                self.pos[1] = x.rect[1] - 0.1 -30 #在距離內 移至bar上方
                return [True, x.color]
        return [False, None]

    def row_up(self, is_collap):#[bool, color]
        if is_collap[0]:
            self.pos[1] -= 0.8
            if is_collap[1] == red:
                self.touch_red()
            if is_collap[1] == white:
                self.touch_white()
            win.blit(self.img, self.pos)

    def touch_red(self):#touch red bar go right
        self.pos[0] += 3
    def touch_white(self):
        self.pos[0] -= 3

class bar:
    def __init__(self):
        self.size = [100, 30]
        self.color = bar_class[random.randint(0, 2)]
        self.rect = pygame.rect.Rect([0, 800], self.size)
        self.ran_pos = [random.randint(0,500)] + [0]

    def show(self):
        p = self.ran_pos
        try:
            pygame.draw.rect(win, self.color, ((self.rect[0] + p[0], self.rect[1] + p[1]), self.size))
            #pygame.display.update(pygame.draw.rect(win, self.color, ((self.rect[0] + p[0], self.rect[1] + p[1]), self.size)))
        except:
            pass
    
    def row_up(self):
        self.rect.move_ip(0, -1)


class add_rect_right:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pygame.rect.Rect(self.pos, self.size)
    
    def draw(self):
        pygame.draw.rect(right_surface, self.rect)
       
                




pygame.time.set_timer(pygame.USEREVENT + 1, 600)
pygame.draw
game_start = False
game_loop = True

while game_loop:
    p1 = people()
    move = [False, False]
    bars = []
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_start = True


    win.fill(black)
    while game_start:
        win.fill(black)
        win.blit(right_surface, (600, 0))
        #right_surface.blit(p1.img, (0, 0))
        b1 = bar()
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT]:
                move[1] = True
            if key[pygame.K_LEFT]:
                move[0] = True
            if event.type == pygame.KEYUP:
                move = [False, False]
            if event.type == pygame.USEREVENT + 1:
                a = random.randint(0, 1)
                if a == 1:
                    bars.append(b1)
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        if True in move:
            p1.move(move)

        for x in bars:
            x.row_up()
            if x.rect[1] <= 0:
                del bars[0]
        for x in bars:
            x.show()

        #是否撞到bar
        p1.row_up(p1.is_collapse(bars))
           
        if not p1.drop_down():
            game_start = False
            print('game over')
        clock.tick(200)
        pygame.display.update()
    #win.fill(blue)