import pygame

# Define `play` global para rastrear o estado do jogo entre o menu e o jogo
play = False

def menu(ecra, largura_ecra, altura_ecra, fundo):
    global play  # Usa `play` como variável global

    pygame.font.init()
    font_titulo = pygame.font.Font("fonts/Saiyan-Sans.ttf", 100)  # Fonte para o título
    font_botoes = pygame.font.Font("fonts/Saiyan-Sans.ttf", 60)   # Fonte para os botões

    # Texto do título
    titulo_text = font_titulo.render("Goku Invaders", True, (255, 255, 255))
    titulo_rect = titulo_text.get_rect(center=(largura_ecra // 2, altura_ecra // 4.5))

    # Definindo as cores
    botao_cor = (166, 148, 131)
    botao_hover_cor = (255, 70, 70)
    sombra_cor = (50, 50, 50)

    # Texto do botão principal com base no estado do jogo
    texto_play_resume = "Resume" if play else "Play"

    # Botões e suas posições
    botoes = {
        texto_play_resume: (largura_ecra // 2, altura_ecra // 2),
        "Score": (largura_ecra // 2, altura_ecra // 2 + 100),
        "Quit": (largura_ecra // 2, altura_ecra // 2 + 200)
    }

    # Dimensões fixas dos botões (largura e altura)
    largura_botao = 140
    altura_botao = 70

    # Loop principal do menu
    while True:
        ecra.blit(fundo, (0, 0))  # Fundo do menu
        ecra.blit(titulo_text, titulo_rect)  # Título no topo

        # Checa a posição do mouse para os efeitos de hover
        mouse_pos = pygame.mouse.get_pos()

        for texto, posicao in botoes.items():
            # Renderizar o texto do botão
            botao_texto = font_botoes.render(texto, True, (255, 255, 255))

            # Definir retângulo do botão com largura e altura fixas
            botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
            botao_rect.center = posicao

            # Caixa de sombra
            sombra_rect = botao_rect.copy()
            sombra_rect.topleft = (botao_rect.topleft[0] + 4, botao_rect.topleft[1] + 4)
            pygame.draw.rect(ecra, sombra_cor, sombra_rect, border_radius=12)

            # Efeito de hover (mudança de cor e "elevação" da caixa do botão)
            if botao_rect.collidepoint(mouse_pos):
                pygame.draw.rect(ecra, botao_hover_cor, botao_rect, border_radius=12)
            else:
                pygame.draw.rect(ecra, botao_cor, botao_rect, border_radius=12)

            # Desenha o texto do botão centralizado dentro do retângulo
            botao_texto_rect = botao_texto.get_rect(center=botao_rect.center)
            ecra.blit(botao_texto, botao_texto_rect)

        # Detecta eventos de clique nos botões
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Checa cada botão individualmente
                for texto, posicao in botoes.items():
                    botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
                    botao_rect.center = posicao
                    if botao_rect.collidepoint(evento.pos):
                        if texto == "Play" or texto == "Resume":
                            play = True  # Define `play` como True ao clicar em "Play" ou "Resume"
                            return "play"
                        elif texto == "Score":
                            return "score"
                        elif texto == "Quit":
                            pygame.quit()
                            return "quit"

        pygame.display.update()
