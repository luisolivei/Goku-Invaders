import pygame

# tamanho tela
x = 800
y = 600


pygame.init()

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Goku-Invaders")

bg = pygame.image.load("images/bg.png").convert_alpha() #imagem de fundo tela
bg = pygame.transform.scale(bg, (x, y))

playerImage = pygame.image.load("images/gk-fly.png").convert_alpha()
playerImage = pygame.transform.scale(playerImage, (50, 50))
playerImage = pygame.transform.rotate(playerImage, 0)

pos_player_x = 100
pos_player_y = y/2-25

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

    # definição de teclas para movimentar o player
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
    if tecla[pygame.K_DOWN] and pos_player_y < y - 50:
        pos_player_y += 1

#Velocidade movimento tela
    x -= 0.2

    screen.blit(playerImage, (pos_player_x, pos_player_y))

    pygame.display.update()

pygame.quit()