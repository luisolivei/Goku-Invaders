import pygame

def menu(ecra, largura_ecra, altura_ecra, fundo):
    font = pygame.font.Font(None, 74)
    play_text = font.render("Play", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(largura_ecra // 2, altura_ecra // 2))
    
    while True:
        ecra.blit(fundo, (0, 0))  # Fundo do menu
        ecra.blit(play_text, play_rect)  # Texto "Play" no centro da tela

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(evento.pos):
                    return True  # Inicia o jogo se "Play" for clicado

        pygame.display.update()
