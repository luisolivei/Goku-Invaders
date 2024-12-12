import pygame

def fade_in_out(ecra, cor, largura, altura, tempo):
    fade_surface = pygame.Surface((largura, altura))
    fade_surface.fill(cor)

    # Fade-in: aumenta a opacidade gradualmente
    for alpha in range(0, 256, 6):  # Ajuste o passo (5) para a velocidade de fade desejada
        fade_surface.set_alpha(alpha)
        ecra.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(int(tempo / 55))  # Ajuste a duração conforme necessário

    # Fade-out: diminui a opacidade gradualmente
    for alpha in range(255, -1, -6):
        fade_surface.set_alpha(alpha)
        ecra.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(int(tempo / 55))