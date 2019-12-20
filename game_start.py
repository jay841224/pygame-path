import pygame
import numpy as np
pygame.init()

def define_block():
    draw = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
        while draw:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    draw = False
            if mouse[1] > 40:
                x = mouse[0]//4
                y = mouse[1]//4
                pygame.draw.rect(background, [255, 0, 0], ((4*x, 4*y), (4, 4)))
                screen.blit(background, (0, 0))
                pygame.display.update()
            
                


def start_window(size):
    screen = pygame.display.set_mode(size)
    background = pygame.display.set_mode(size)
    return screen, background

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

class Dijkstra:
    def __init__(self, ox, oy):
        self.ox = ox
        self.oy = oy

    class Node:
        def __init__(self, x, y, cost, pind):
            self.x = x
            self.y = y
            self.cost = cost
            self.pind = pind


    def planning(self, sx, sy, gx, gy):
        


screen, background = start_window((400, 440))
white = [255, 255, 255]
blue = [0, 0, 150]
black = [0, 0, 0]
#window set button
choose_start_but = button(white, 0, 0, 80, 40, text='choose start')
choose_start_but.draw(background, black)
choose_end_but = button(blue, 80, 0, 80, 40, text='choose end')
choose_end_but.draw(background, white)
draw_block_but = button(white, 160, 0, 80, 40, text='draw block')
draw_block_but.draw(background, black)

for row in range(100):
    for col in range(10, 110):
        pygame.draw.rect(background, [25, 80, 50], ((row*4, col*4), (4, 4)))
        pygame.draw.rect(background, [0, 0, 0], ((row*4, col*4), (4, 4)), 1)

screen.blit(background, (0, 0))
pygame.display.update()



run = True
while run:
    define_block()
    pygame.display.update()