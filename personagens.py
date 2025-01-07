# personagens.py contém classes e subclasses aninhadas do personagem principal

import pygame
from config import velocidade_animacao

class Personagem:
    def __init__(self, caminhos_sprites, cor_chave=(144, 176, 216)):
        # Inicializa a lista de sprites e outros parâmetros de animação
        self.sprites = []
        self.indice_sprite = 0
        self.tempo_desde_ultimo_sprite = 0
        self.velocidade_animacao = velocidade_animacao
        self.carregar_sprites(caminhos_sprites, cor_chave)

    def carregar_sprites(self, caminhos_sprites, cor_chave):
        # Carrega cada sprite de acordo com os caminhos especificados
        for caminho in caminhos_sprites:
            sprite = pygame.image.load(caminho).convert()
            sprite.set_colorkey(cor_chave)  # Define a cor-chave para transparência
            self.sprites.append(sprite)

    def reiniciar(self):
        # Reinicia a animação para o primeiro sprite
        self.indice_sprite = 0
        self.tempo_desde_ultimo_sprite = 0

    def atualizar(self, delta_tempo):
        # Atualiza o índice de sprite baseado no tempo para animar
        self.tempo_desde_ultimo_sprite += delta_tempo
        if self.tempo_desde_ultimo_sprite >= self.velocidade_animacao:
            self.indice_sprite = (self.indice_sprite + 1) % len(self.sprites)
            self.tempo_desde_ultimo_sprite = 0

    def obter_sprite_atual(self):
        # Retorna o sprite atual a ser exibido
        return self.sprites[self.indice_sprite]

# Animação do estado parado
class AnimacaoParado(Personagem):
    def __init__(self):
        caminhos_sprites = [
            "imagens/goku/parado/parado_1.gif",
        ]
        super().__init__(caminhos_sprites)

# Animação do estado de andar
class AnimacaoAndar(Personagem):
    def __init__(self):
        caminhos_sprites = [
            "imagens/goku/parado/parado_1.gif",
        ]
        super().__init__(caminhos_sprites)

# Animação do estado de disparo
class AnimacaoDisparar(Personagem):
    def __init__(self):
        caminhos_sprites = [
            "imagens/goku/disparar/disparar_1.gif",
            "imagens/goku/disparar/disparar_2.gif",
            "imagens/goku/disparar/disparar_3.gif",
            "imagens/goku/disparar/disparar_4.gif",
            "imagens/goku/disparar/disparar_5.gif",
        ]
        super().__init__(caminhos_sprites)

# Animação do estado de atingido
class AnimacaoAtingido(Personagem):
    def __init__(self):
        caminhos_sprites = [
            "imagens/goku/atingido/atingido_6.gif",
        ]
        super().__init__(caminhos_sprites)

class AnimacaoDispararEspecial(Personagem):
    def __init__(self):
        caminhos_sprites = [
            f"imagens/goku/projectil2/animacao_disparar2_{i}.gif" for i in range(1, 13)
        ]
        super().__init__(caminhos_sprites)