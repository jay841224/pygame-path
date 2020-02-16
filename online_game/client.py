import pygame

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
        self.rect = (self.x, self.y, self.width, self.heigh)
        
def redrawWindow(win, player):
    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()


def main():
    run = True
    p = player(50, 50, 100, 100, (0, 255, 0))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)

main()