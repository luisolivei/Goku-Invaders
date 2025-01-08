#inimigos.py

import pygame
from config import largura_ecra, altura_ecra
from projetil import Projetil, Projetil2
import random

class Inimigo:
    def __init__(self, tipo, pos_y, cores_fundo=[(132, 66, 4), (128, 0, 128), (153, 217, 234),(96, 64, 168),(84, 109, 142),(96, 64, 168)]):
        self.tipo = tipo
        self.vidas = {1: 3, 2: 5, 3: 7, 4: 5, 5: 3}[tipo]
        self.pos_x = largura_ecra
        self.pos_y = pos_y
        self.cores_fundo = cores_fundo
        self.direcao_sprite = 1

        self.escalas = {1: 50, 2: 100, 3: 100, 4:100, 5:80}
        self.escala = self.escalas.get(tipo, 100) / 100

        self.velocidade = 1

        self.velocidades_animacoes = {
            1: {"andar": 0.2, "morto": 0.1},
            2: {"andar": 0.3, "morto": 0.1},
            3: {"andar": 0.5, "morto": 0.2},
            4: {"andar": 0.3, "morto": 0.3},
            5: {"andar": 0.3, "morto": 0.1},
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

    def carregar_sprites(self, estado, tipos_ficheiro=("gif", "png"), num_maximo=10):
        sprites = []
        for i in range(1, num_maximo + 1):
            for tipo in tipos_ficheiro:
                caminho = f"imagens/Inimigos/inimigo_{self.tipo}/inimigo_{self.tipo}_{estado}_{i}.{tipo}"
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

class InimigoFinal:
    def __init__(self, x, y, altura_ecra, cores_fundo=[(132, 66, 4)]):
        self.x = x
        self.y = y
        self.velocidade = 3
        self.vidas = 200
        self.vivo = True
        self.projeteis = []  # Lista para armazenar projéteis do inimigo
        self.tempo_desde_ultimo_disparo = 0  # Controle do tempo entre disparos
        self.cores_fundo = cores_fundo  # Atributo cores_fundo inicializado corretamente
        self.altura_ecra = altura_ecra  # Definir a altura da tela
        self.sprites = self.carregar_sprites()  # Agora, a inicialização está completa antes do uso
        self.indice_sprite = 0  # Índice do sprite atual
        self.direcao_sprite = 1  # 1 para frente, -1 para trás
        self.tempo_animacao = 0  # Controle do tempo de animação
        self.velocidade_animacao = 500  # Velocidade da animação (em milissegundos)
        self.largura = 100  # Largura do sprite do inimigo
        self.altura = 150  # Altura do sprite do inimigo

    def carregar_sprites(self):
        sprites = []
        for i in range(1, 6):
            sprite = pygame.image.load(f"imagens/inimigos/inimigo_final/final_{i}.png").convert_alpha()
            sprite = self.remover_cores_fundo(sprite, self.cores_fundo)  # Passa cores_fundo explicitamente
            sprites.append(sprite)
        return sprites

    def atualizar(self, delta_tempo):
        if not self.vivo:
            return

        # Atualiza o tempo de animação
        self.tempo_animacao += delta_tempo * 1000  # Converte delta_tempo para milissegundos

        # Se o tempo de animação tiver passado o suficiente, muda o sprite
        if self.tempo_animacao >= self.velocidade_animacao:
            self.indice_sprite += self.direcao_sprite

            # Reseta o tempo de animação
            self.tempo_animacao = 0

            # Se o índice do sprite chegar ao final ou ao início, inverte a direção
            if self.indice_sprite >= len(self.sprites):
                self.direcao_sprite = -1
                self.indice_sprite = len(self.sprites) - 2  # Evita ultrapassar o índice
            elif self.indice_sprite < 0:
                self.direcao_sprite = 1
                self.indice_sprite = 1  # Evita ultrapassar o índice

        # Movimento vertical aleatório
        if random.randint(1, 100) <= 5:  # Pequena chance de mudar direção
            self.velocidade *= -1
        self.y += self.velocidade
        if self.y < 0 or self.y > self.altura_ecra - 150:  # Corrigido para usar self.altura_ecra
            self.velocidade *= -1

        # Disparo de projéteis
        self.tempo_desde_ultimo_disparo += delta_tempo
        if self.tempo_desde_ultimo_disparo >= 2:  # Dispara a cada 2 segundos
            self.disparar()
            self.tempo_desde_ultimo_disparo = 0

        # Atualiza os projéteis
        for projetil in self.projeteis[:]:
            projetil.atualizar()
            if projetil.saiu_do_ecra():  # Remove projéteis que saíram da tela
                self.projeteis.remove(projetil)

    def disparar(self):
        novo_projetil = Projetil(self.x - 20, self.y + 32, velocidade=5, sentido="esquerda")
        self.projeteis.append(novo_projetil)

    def desenhar(self, ecra):
        if self.vivo:
            sprite = self.sprites[self.indice_sprite]  # Exibe o sprite atual
            ecra.blit(sprite, (self.x, self.y))

        # Desenha os projéteis
        for projetil in self.projeteis:
            projetil.desenhar(ecra)

    def verificar_colisao(self, projetil):
        if isinstance(projetil, Projetil2):
            # Usa o método verificar_colisao do projetil
            if projetil.verificar_colisao(self):
                self.vidas -= 1
                if self.vidas <= 0:
                    self.vivo = False
                return True
        else:
            # Colisão com outros tipos de projéteis
            if pygame.Rect(self.x, self.y, self.largura, self.altura).colliderect(
                pygame.Rect(projetil.x, projetil.y, 32, 32)
            ):
                self.vidas -= 1
                if self.vidas <= 0:
                    self.vivo = False
                return True
        return False
    
    def remover_cores_fundo(self, sprite, cores_fundo):
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                cor = sprite.get_at((x, y))
                if cor[0:3] in cores_fundo:  # Usa cores_fundo diretamente aqui
                    sprite.set_at((x, y), (0, 0, 0, 0))
        return sprite
