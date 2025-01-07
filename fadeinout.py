#fadeinout.py serve para suavizar tranziçoes de ecras

import pygame
# Função de fade-in e fade-out
def fade_in_out(ecra, cor, largura, altura, tempo):
    fade_surface = pygame.Surface((largura, altura)) # Cria uma superficie para o efeito
    fade_surface.fill(cor) # Preenche com a cor

    # Fade-in: aumenta a opacidade gradualmente
    for alpha in range(0, 256, 6):  # Aumenta a opacidade em 6 em 6
        fade_surface.set_alpha(alpha) # Define a opacidade
        ecra.blit(fade_surface, (0, 0)) # Desenha
        pygame.display.update() # Atualiza
        pygame.time.delay(int(tempo / 55))  # Tempo de espera

    # Fade-out: diminui a opacidade gradualmente
    for alpha in range(255, -1, -6):  # Diminui a opacidade em 6 em 6
        fade_surface.set_alpha(alpha) # Define a opacidade
        ecra.blit(fade_surface, (0, 0)) # Desenha
        pygame.display.update() # Atualiza
        pygame.time.delay(int(tempo / 55))  # Tempo de espera