import pygame
 
# Inicia o mixer
pygame.mixer.init()
 
# Carrega e gerencia os sons
class Sons:
    def __init__(self):

        # Dicionário com músicas por nível
        self.musicas = {
            1: "Sons/musica_nivel.mp3",
            2: "Sons/musica_nivel2.mp3",
            3: "Sons/musica_ultimo_nivel.mp3"
        }
        # Sons de efeitos
        self.som_disparo = pygame.mixer.Sound("Sons/disparos.mp3")
        self.som_disparo.set_volume(0.7)  # Ajusta o volume do disparo
        self.som_colisao = pygame.mixer.Sound("Sons/colisao.mp3")
        self.som_colisao.set_volume(0.8)  # Ajusta o volume da colisão
 
        self.som_game_over = pygame.mixer.Sound("Sons/game_over.mp3")
        self.som_game_over.set_volume(1.0)  # Ajusta o volume do game over
 
    def tocar_musica_menu(self):
        pygame.mixer.music.load("Sons/som_menu.mp3")  # Chama a música do menu
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Inicia a música em loop

    def tocar_musica_fundo(self, nivel):
        if nivel in self.musicas:
            pygame.mixer.music.load(self.musicas[nivel])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

    def parar_musica_fundo(self):
        pygame.mixer.music.stop()  # Para a música de fundo
 
    def tocar_disparo(self):
        self.som_disparo.play()
 
    def tocar_colisao(self):
        self.som_colisao.play()
 
    def tocar_game_over(self):
        self.som_game_over.play()