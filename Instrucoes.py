import pygame
from config import largura_ecra, altura_ecra, caminho_fonte
def tela_instrucoes(ecra, largura_ecra, altura_ecra):
    """Exibe as teclas antes de iniciar o jogo."""
    # Carregar os ícones das teclas
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

    # Posições dos ícones e textos
    pos_up = (10, altura_ecra - 200)
    pos_down = (10, altura_ecra - 160)
    pos_space = (10, altura_ecra - 120)

    # Fonte e textos explicativos
    fonte = pygame.font.Font(caminho_fonte, 32)
    texto_up = fonte.render("Mover para cima", True, (255, 255, 255))
    texto_down = fonte.render("Mover para baixo", True, (255, 255, 255))
    texto_space = fonte.render("Atirar", True, (255, 255, 255))
    texto_iniciar = fonte.render("Pressione ENTER para começar", True, (255, 165, 0))

    # Fundo da tela
    fundo = pygame.image.load("images/imagem_inicial.jpg").convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

    # Loop da tela de teclas
    while True:
        ecra.blit(fundo, (0, 0))  # Desenha o fundo
        ecra.blit(icone_up, pos_up)
        ecra.blit(icone_down, pos_down)
        ecra.blit(icone_space, pos_space)
        ecra.blit(texto_up, (70, altura_ecra - 200))
        ecra.blit(texto_down, (70, altura_ecra - 160))
        ecra.blit(texto_space, (120, altura_ecra - 120))
        ecra.blit(texto_iniciar, (largura_ecra // 2 - texto_iniciar.get_width() // 2, altura_ecra - 60))

        pygame.display.flip()  # Atualiza a tela

        # Lógica para mostrar as instruções
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # ENTER para começar
                        return  # Sai da função e indica que o jogador está pronto