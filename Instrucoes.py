#Instrucoes.py ecra de instruçoes antes de iniciar propriamente o jogo

import pygame
from config import caminho_fonte

def tela_instrucoes(ecra, largura_ecra, altura_ecra):
    # Carregar os ícones das teclas
    icone_up = pygame.transform.scale(
        pygame.image.load("imagens/icons/Teclas/up.png").convert_alpha(),
        (50, 50)
    )
    icone_down = pygame.transform.scale(
        pygame.image.load("imagens/icons/Teclas/down.png").convert_alpha(),
        (50, 50)
    )
    icone_space = pygame.transform.scale(
        pygame.image.load("imagens/icons/Teclas/space.png").convert_alpha(),
        (100, 50)
    )
    icone_x = pygame.transform.scale(
        pygame.image.load("imagens/icons/Teclas/x.png").convert_alpha(),
        (50, 50)
    )

    # Posições dos ícones e textos
    pos_up = (10, altura_ecra - 240)
    pos_down = (10, altura_ecra - 200)
    pos_space = (10, altura_ecra - 160)
    pos_x = (10, altura_ecra - 120)

    # Fonte e textos explicativos
    fonte = pygame.font.Font(caminho_fonte, 32)
    texto_up = fonte.render("Mover para cima", True, (255, 255, 255)) # Branco
    texto_down = fonte.render("Mover para baixo", True, (255, 255, 255)) # Branco
    texto_space = fonte.render("Atirar", True, (255, 255, 255)) # Branco
    texto_iniciar = fonte.render("Pressione ENTER para começar", True, (255, 165, 0)) # Laranja
    texto_x = fonte.render("Acumula 3 inimigos mortos e desbloqueia Kamehameh", True, (255, 255, 255)) # Branco

    # Criando sombras para os textos (cor preta, deslocada para baixo e à direita)
    cor_sombra = (0, 0, 0)
    texto_up_sombra = fonte.render("Mover para cima", True, cor_sombra)
    texto_down_sombra = fonte.render("Mover para baixo", True, cor_sombra)
    texto_space_sombra = fonte.render("Atirar", True, cor_sombra)
    texto_iniciar_sombra = fonte.render("Pressione ENTER para começar", True, cor_sombra)
    texto_x_sombra = fonte.render("Acumula 3 inimigos mortos e desbloqueia Kamehameh", True, cor_sombra)

    # Fundo da tela
    fundo = pygame.image.load("imagens/Backgrounds/imagem_inicial.jpg").convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

    # Loop da tela de teclas
    while True:
        ecra.blit(fundo, (0, 0))  # Desenha o fundo
        ecra.blit(icone_up, pos_up)
        ecra.blit(icone_down, pos_down)
        ecra.blit(icone_space, pos_space)
        ecra.blit(icone_x, pos_x)

        # Desenhando a sombra dos textos ligeiramente deslocada
        ecra.blit(texto_up_sombra, (70 + 2, altura_ecra - 230 + 2))
        ecra.blit(texto_down_sombra, (70 + 2, altura_ecra - 190 + 2))
        ecra.blit(texto_space_sombra, (120 + 2, altura_ecra - 150 + 2))
        ecra.blit(texto_x_sombra, (70 + 2, altura_ecra - 110 + 2))
        ecra.blit(texto_iniciar_sombra, (largura_ecra // 2 - texto_iniciar.get_width() // 2 + 2, altura_ecra - 60 + 2))

        # Desenhando o texto real
        ecra.blit(texto_up, (70, altura_ecra - 230))
        ecra.blit(texto_down, (70, altura_ecra - 190))
        ecra.blit(texto_space, (120, altura_ecra - 150))
        ecra.blit(texto_x, (70, altura_ecra - 110))
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
