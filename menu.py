import pygame


def menu(ecra, largura_ecra, altura_ecra, fundo):
    pygame.font.init()
    font_titulo = pygame.font.Font(None, 100)  # Fonte para o título
    font_botoes = pygame.font.Font(None, 74)   # Fonte para os botões

    # Texto do título
    titulo_text = font_titulo.render("Goku Invaders", True, (255, 255, 255))
    titulo_rect = titulo_text.get_rect(center=(largura_ecra // 2, altura_ecra // 3))

    # Botão "Play"
    play_text = font_botoes.render("Play", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(largura_ecra // 2, altura_ecra // 2))

    # Botão "Score"
    score_text = font_botoes.render("Score", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(largura_ecra // 2, altura_ecra // 2 + 100))

    # Botão "Quit"
    quit_text = font_botoes.render("Quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(largura_ecra // 2, altura_ecra // 2 + 200))

    while True:
        ecra.blit(fundo, (0, 0))  # Fundo do menu
        ecra.blit(titulo_text, titulo_rect)  # Texto do título no topo

        # Desenhar botões
        ecra.blit(play_text, play_rect)
        ecra.blit(score_text, score_rect)
        ecra.blit(quit_text, quit_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(evento.pos):
                    return "play"  # Inicia o jogo
                elif score_rect.collidepoint(evento.pos):
                    return "score"  # Mostra a pontuação
                elif quit_rect.collidepoint(evento.pos):
                    pygame.quit()
                    return "quit"  # Sai do jogo

        pygame.display.update()
