import pygame
from config import largura_ecra, altura_ecra, caminho_fonte, DURACAO_MOSTRAR_TECLAS,tempo_inicio_jogo
def mostrar_teclas(ecra):
    global tempo_inicio_jogo

    if tempo_inicio_jogo == 0:
        tempo_inicio_jogo = pygame.time.get_ticks()

    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_inicio_jogo > DURACAO_MOSTRAR_TECLAS:
        return

    icone_up = pygame.transform.scale(
        pygame.image.load("images/Teclas/up.png").convert_alpha(),
        (50, 50)
    )
    icone_down = pygame.transform.scale(
        pygame.image.load("images/Teclas/down.png").convert_alpha(),
        (50, 50)
    )
    icone_space = pygame.transform.scale(
        pygame.image.load("images/Teclas/space.png").convert_alpha(),
        (100, 50)
    )

    pos_up = (10, altura_ecra - 200)
    pos_down = (10, altura_ecra - 160)
    pos_space = (10, altura_ecra - 130)

    ecra.blit(icone_up, pos_up)
    ecra.blit(icone_down, pos_down)
    ecra.blit(icone_space, pos_space)

    fonte = pygame.font.Font(caminho_fonte, 24)
    texto_up = fonte.render("Mover para cima", True, (255, 255, 255))
    texto_down = fonte.render("Mover para baixo", True, (255, 255, 255))
    texto_space = fonte.render("Atirar", True, (255, 255, 255))

    ecra.blit(texto_up, (70, altura_ecra - 200))
    ecra.blit(texto_down, (70, altura_ecra - 160))
    ecra.blit(texto_space, (120, altura_ecra - 130))

    pygame.display.update()