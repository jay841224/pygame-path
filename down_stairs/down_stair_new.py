import pygame
import numpy as np
import random, time
from pygame.locals import*
pygame.init()
win = pygame.display.set_mode((800, 800), 0, 32)
#color set
black = [0, 0, 0]
blue = [0, 0, 255]
red = [255, 0, 0]
white = [255, 255, 255]
bar_class = [blue, red, white]


#surface set
win.fill(white)
win2 = pygame.Surface((600, 750))
win2.fill(black)

right_surface = pygame.Surface((200, 200))
right_surface.fill([0, 58, 0])

clock = pygame.time.Clock()
win.blit(win2, (0, 50))
win.blit(right_surface, (600, 0))


def blit_img(path, size, pos):
    raw = pygame.image.load(r'{}'.format(path)).convert_alpha()
    img = pygame.transform.scale(raw, size)
    win.blit(img, pos)


#charactor
class People:
    def __init__(self):
        self.raw_image = pygame.image.load(r'D:\python_game\down_stairs\pacman.png').convert_alpha()
        self.img = pygame.transform.scale(self.raw_image, (30, 30))
        self.pos = [win2.get_size()[0] / 2, win2.get_size()[1] / 8]

    def move(self, direct):
        velocity_r = 3
        velocity_l = -3
        if self.pos[0] >= win2.get_width() - 30:
            velocity_r = 0
        elif self.pos[0] <= 0:
            velocity_l = 0

        if direct[0]:
            self.pos[0] += velocity_l
        if direct[1]:
            self.pos[0] += velocity_r
        win2.blit(self.img, self.pos)
    
    def drop_down(self):
        gravity = 1
        self.pos[1] += gravity
        #win.fill(black)
        win2.blit(self.img, self.pos)
        if self.pos[1] > win2.get_size()[1]:
            alter_blood(100)
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
        if is_collap[0]:#blooooooooooooooooooooooooooood
            self.pos[1] -= 0.8
            if self.pos[1] <= 0:
                self.pos[1] += 10
                alter_blood(30)
                win2.blit(self.img, self.pos)

            if is_collap[1] == red:
                self.touch_red()
            if is_collap[1] == white:
                self.touch_white()
            win2.blit(self.img, self.pos)


    def touch_red(self):#touch red bar go right
        self.pos[0] += 3
    def touch_white(self):
        self.pos[0] -= 3

class bar:
    def __init__(self):
        self.size = [100, 30]
        self.color = bar_class[random.randint(0, 2)]
        self.rect = pygame.rect.Rect([0, 800], self.size)
        self.ran_pos = [random.randint(30,470)] + [0]
        p = self.ran_pos
        self.root_right_arrow = [[self.rect[0] + p[0], self.rect[1] + p[1] + 10], [self.rect[0] + p[0], self.rect[1] + p[1] + 20], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 20], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 25],
                     [self.rect[0] + p[0] + 20, self.rect[1] + p[1] + 15], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 5], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 10]]
        self.right_arrow = [[self.rect[0] + p[0], self.rect[1] + p[1] + 10], [self.rect[0] + p[0], self.rect[1] + p[1] + 20], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 20], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 25],
                     [self.rect[0] + p[0] + 20, self.rect[1] + p[1] + 15], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 5], [self.rect[0] + p[0] + 15, self.rect[1] + p[1] + 10]]
        

        self.root_left_arrow = []
        self.left_arrow = []
        
        for r in self.root_right_arrow:
            self.root_left_arrow.append([self.ran_pos[0] + self.size[0] - (r[0] - self.ran_pos[0]), r[1]])
            self.left_arrow.append([self.ran_pos[0] + self.size[0] - (r[0] - self.ran_pos[0]), r[1]])
        

    def show(self):
        p = self.ran_pos
        try:
            pygame.draw.rect(win2, self.color, ((self.rect[0] + p[0], self.rect[1] + p[1]), self.size))
            if self.color == red:
                pygame.draw.polygon(win2, (0, 255, 255), self.right_arrow)
            if self.color == white:
                pygame.draw.polygon(win2, (0, 255, 0), self.left_arrow)

            #pygame.draw.rect(win2, self.color, self.rect)
            #pygame.display.update(pygame.draw.rect(win, self.color, ((self.rect[0] + p[0], self.rect[1] + p[1]), self.size)))
        except:
            pass
    
    def row_up(self):
        self.rect.move_ip(0, -1)
        step = 0
        arrow = None
        root_arrow = None
        if self.color == red:
            step = 1
            arrow = self.right_arrow
            root_arrow = self.root_right_arrow
        if self.color == white:
            step = -1
            arrow = self.left_arrow
            root_arrow = self.root_left_arrow
        
        if arrow != None:
            for r in arrow:
                r[1] -= 1
                r[0] += step
            if arrow[4][0] >= self.ran_pos[0] + self.size[0] or arrow[4][0] <= self.ran_pos[0]:
                for r, w in zip(arrow, root_arrow):
                    r[0] = w[0]
                #箭頭超出後返回
        else:
            pass

class create_rect:
    def __init__(self, color, size, pos, w):
        self.color = color
        self.size = size
        self.pos = pos
        self.w = w

    def show(self, i=0):
        self.size[0] -= i
        if self.size[0] <= 0:
            self.size[0] = 0
        pygame.draw.rect(self.w, self.color, (self.pos, self.size))
        #pygame.draw.rect(self.w, self.color, (self.pos, self.size))
        


def alter_blood(i=0):
    #blood_background = create_rect(white, (50, 100), (50, 100), right_surface)
    right_surface.fill([0, 58, 0])
    blood_background.show()
    blood.show(i)
    win.blit(right_surface, (600, 0))









pygame.time.set_timer(pygame.USEREVENT + 1, 500)
game_loop = True
game_start = False
#add jagged img on top
for i in range(0, 600, 50):
    blit_img(r'D:\python_game\down_stairs\triangle.png', (50, 50), (i, 0))

while game_loop:
    p1 = People()
    move = [False, False]
    bars = []
    #rect for blood
    blood = create_rect(red, [100, 50], [50, 75], right_surface)
    blood_background = create_rect(white, [100, 50], [50, 75], right_surface)
    alter_blood()
    
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_start = True
    
    while game_start:
        win2.fill(black)
        win2.blit(p1.img, p1.pos)
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

        if not p1.drop_down() or blood.size[0] == 0:#終止條件
            game_start = False
            print('game over')


        win.blit(win2, (0, 50))
        clock.tick(200)
        pygame.display.flip()
        #pygame.display.update()