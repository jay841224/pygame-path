import pygame
from network import Network

width = 500
heigh = 500
win = pygame.display.set_mode((width, heigh))
pygame.display.set_caption('Client')

clientNumber = 0

class player():
    def __init__(self, x, y, width, heigh, color):
        self.x = x
        self.y = y
        self.width = width
        self.heigh = heigh
        self.color = color
        self.rect = (x, y, width, heigh)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.x -= self.vel
        if key[pygame.K_RIGHT]:
            self.x += self.vel
        if key[pygame.K_UP]:
            self.y -= self.vel
        if key[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.heigh)

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])
        
def redrawWindow(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPoint = read_pos(n.getPos())
    p = player(startPoint[0], startPoint[1], 100, 100, (0, 255, 0))
    p2 = player(0, 0, 100, 100, (255, 0, 0))
    
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)

main()