#sons.py gere sequencias sons

import pygame

# Inicia o mixer
pygame.mixer.init()

# Carrega e gerencia os sons
class Sons:
    def __init__(self):
        self.mutado = False  # Atributo para controlar o estado do mute

        # Dicionário com músicas por nível
        self.musicas = {
            1: "Sons/musica_nivel.mp3",
            2: "Sons/musica_nivel2.mp3",
            3: "Sons/musica_ultimo_nivel.mp3",
            4: "Sons/musica_final.mp3",
            5: "Sons/creditos.mp3"
        }
        # Sons de efeitos
        self.som_disparo = pygame.mixer.Sound("Sons/disparos.mp3")
        self.som_disparo.set_volume(0.2)  # Ajusta o volume do disparo
        self.som_disparo2 = pygame.mixer.Sound("Sons/kamehameha.mp3")
        self.som_disparo2.set_volume(0.2)  # Ajusta o volume do disparo2
        self.som_colisao = pygame.mixer.Sound("Sons/colisao.mp3")
        self.som_colisao.set_volume(0.2)  # Ajusta o volume da colisão

        self.som_game_over = pygame.mixer.Sound("Sons/game_over.mp3")
        self.som_game_over.set_volume(1.0)  # Ajusta o volume do game over

    # Método para mutar todos os sons
    def ligar(self):
        self.mutado = True
        pygame.mixer.music.set_volume(0)  # Desativa o volume da música
        self.som_disparo.set_volume(0)  # Desativa o volume do disparo
        self.som_disparo2.set_volume(0)  # Desativa o volume do disparo2
        self.som_colisao.set_volume(0)  # Desativa o volume da colisão
        self.som_game_over.set_volume(0)  # Desativa o volume do game over

    # Método para desmutar todos os sons
    def desligar(self):
        self.mutado = False
        pygame.mixer.music.set_volume(0.3)  # Restaura o volume da música
        self.som_disparo.set_volume(0.2)  # Restaura o volume do disparo
        self.som_disparo2.set_volume(0.2)  # Restaura o volume do disparo2
        self.som_colisao.set_volume(0.2)  # Restaura o volume da colisão
        self.som_game_over.set_volume(1.0)  # Restaura o volume do game over
    def tocar_musica_menu(self):
        if not self.mutado:
            pygame.mixer.music.load("Sons/som_menu.mp3")  # Chama a música do menu
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Inicia a música em loop

    def tocar_musica_fundo(self, nivel):
        if not self.mutado and nivel in self.musicas:
            pygame.mixer.music.load(self.musicas[nivel])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

    def parar_musica_fundo(self):
        pygame.mixer.music.stop()  # Para a música de fundo

    def tocar_disparo(self):
        if not self.mutado:
            self.som_disparo.play()

    def tocar_disparo2(self):
        if not self.mutado:
            self.som_disparo2.play()

    def tocar_colisao(self):
        if not self.mutado:
            self.som_colisao.play()
        
    def tocar_game_over(self):
        if not self.mutado:
            self.som_game_over.play()