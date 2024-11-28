import pygame
from config import largura_ecra

class Inimigo:
    def __init__(self, tipo, pos_y, cores_fundo=[(132, 66, 4), (128, 0, 128)]):
        self.tipo = tipo
        self.vidas = {1: 3, 2: 5, 3: 7}[tipo]
        self.pos_x = largura_ecra
        self.pos_y = pos_y
        self.cores_fundo = cores_fundo
        self.direcao_sprite = 1

        self.escalas = {1: 50, 2: 100, 3: 100}
        self.escala = self.escalas.get(tipo, 100) / 100

        self.velocidade = 1

        self.velocidades_animacoes = {
            1: {"andar": 0.2, "morto": 0.1},
            2: {"andar": 0.3, "morto": 0.1},
            3: {"andar": 0.5, "morto": 0.1},
        }
        self.velocidade_animacao_atual = self.velocidades_animacoes[self.tipo].get("andar", 0.1)

        self.animacoes = {
            "andar": self.carregar_sprites("andar"),
            "morto": self.carregar_sprites("morto"),
        }
        self.animacao_atual = "andar"
        self.indice_sprite = 0
        self.tempo_desde_ultimo_sprite = 0

        self.vivo = True

    def carregar_sprites(self, estado, tipos_ficheiro=("gif", "png"), num_maximo=6):
        sprites = []
        for i in range(1, num_maximo + 1):
            for tipo in tipos_ficheiro:
                caminho = f"images/Inimigos/inimigo_{self.tipo}/inimigo_{self.tipo}_{estado}_{i}.{tipo}"
                try:
                    sprite = pygame.image.load(caminho).convert_alpha()
                    sprite = self.remover_cores_fundo(sprite)
                    sprite = pygame.transform.flip(sprite, True, False)
                    sprite = self.redimensionar_sprite(sprite)
                    sprites.append(sprite)
                    break
                except FileNotFoundError:
                    continue
        return sprites

    def remover_cores_fundo(self, sprite):
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                cor = sprite.get_at((x, y))
                if cor[0:3] in self.cores_fundo:
                    sprite.set_at((x, y), (0, 0, 0, 0))
        return sprite

    def redimensionar_sprite(self, sprite):
        largura_original, altura_original = sprite.get_size()
        nova_largura = int(largura_original * self.escala)
        nova_altura = int(altura_original * self.escala)
        return pygame.transform.scale(sprite, (nova_largura, nova_altura))

    def atualizar(self, delta_tempo, jogador):
        if not self.vivo:
            return

        self.velocidade_animacao_atual = self.velocidades_animacoes[self.tipo].get(self.animacao_atual, 0.1)
        self.tempo_desde_ultimo_sprite += delta_tempo
        if self.tempo_desde_ultimo_sprite >= self.velocidade_animacao_atual:
            self.tempo_desde_ultimo_sprite = 0

            if self.animacao_atual == "andar":
                self.indice_sprite += self.direcao_sprite
                if self.indice_sprite == len(self.animacoes["andar"]) - 1:
                    self.direcao_sprite = -1
                elif self.indice_sprite == 0:
                    self.direcao_sprite = 1
            else:
                self.indice_sprite = (self.indice_sprite + 1) % len(self.animacoes[self.animacao_atual])

            if self.animacao_atual == "morto" and self.indice_sprite == 0:
                self.vivo = False  # Marca como morto após a animação "morto" ser concluída

        if self.animacao_atual == "andar":
            self.pos_x -= self.velocidade
            if self.pos_x < 0:  # Inimigo saiu pela esquerda ecra
                self.vivo = False
                return "fora"  # Retorna estado saída pela esquerda

    def desenhar(self, ecra):
        if self.vivo:
            sprite = self.animacoes[self.animacao_atual][self.indice_sprite]
            ecra.blit(sprite, (self.pos_x, self.pos_y))

    def verificar_colisao(self, projetil):
        # Ignora colisões enquanto está na animação "morto"
        if not self.vivo or self.animacao_atual == "morto":
            return False

        sprite = self.animacoes[self.animacao_atual][self.indice_sprite]
        inimigo_rect = sprite.get_rect(topleft=(self.pos_x, self.pos_y))
        projetil_rect = projetil.imagem.get_rect(topleft=(projetil.x, projetil.y))

        if inimigo_rect.colliderect(projetil_rect):
            self.vidas -= 1
            if self.vidas <= 0:
                self.animacao_atual = "morto"
                self.indice_sprite = 0
            return True

        return False
