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

    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 800:
        screen.blit(bg, (rel_x, 0))

    x -= 1


    pygame.display.update()

pygame.quit()