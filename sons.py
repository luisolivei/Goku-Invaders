import pygame
 
# Inicia o mixer
pygame.mixer.init()
 
# Carrega e gerencia os sons
class Sons:
    def __init__(self):
        # Música de fundo
        self.som_fundo = "Sons/musica_nivel.mp3"
        pygame.mixer.music.load(self.som_fundo)
        pygame.mixer.music.set_volume(0.5)  # Ajusta o volume da música de fundo
        # Sons de efeitos
        self.som_disparo = pygame.mixer.Sound("Sons/disparos.mp3")
        self.som_disparo.set_volume(0.7)  # Ajusta o volume do disparo
        self.som_colisao = pygame.mixer.Sound("Sons/colisao.mp3")
        self.som_colisao.set_volume(0.8)  # Ajusta o volume da colisão
 
        self.som_game_over = pygame.mixer.Sound("Sons/game_over.mp3")
        self.som_game_over.set_volume(1.0)  # Ajusta o volume do game over
 
    def tocar_musica_fundo(self):
        pygame.mixer.music.play(-1)  # Inicia a música em loop
 
    def parar_musica_fundo(self):
        pygame.mixer.music.stop()  # Para a música de fundo
 
    def tocar_disparo(self):
        self.som_disparo.play()
 
    def tocar_colisao(self):
        self.som_colisao.play()
 
    def tocar_game_over(self):
        self.som_game_over.play()