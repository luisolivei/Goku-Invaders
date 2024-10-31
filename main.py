import pygame

x = 800
y = 600


pygame.init()

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Goku-Invaders")

bg = pygame.image.load("images/bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            
    screen.blit(bg, (0, 0))


    pygame.display.update()

pygame.quit()