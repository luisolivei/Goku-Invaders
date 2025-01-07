# projetil.py contém classes projectil

import pygame
from config import largura_ecra

class Projetil:
    def __init__(self, x, y, velocidade=5, cores_fundo=[(144, 176, 216)],sentido="direita"):
        # Inicializa a posição e velocidade do projetil
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.imagem = pygame.image.load("imagens/projectil/chama_disparos.gif").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (20, 20))  # Ajusta o tamanho da imagem
        self.cores_fundo = cores_fundo
        self.remover_cores_fundo()
        self.sentido = sentido  # "direita" ou "esquerda"

        # Inverte o sprite horizontalmente se o sentido for "esquerda" para inimigo final
        if self.sentido == "esquerda":
            self.imagem = pygame.transform.flip(self.imagem, True, False)

    
    def remover_cores_fundo(self):
        # Converte a imagem para acesso direto aos pixels
        self.imagem = self.imagem.convert_alpha()
        largura, altura = self.imagem.get_size()
        for x in range(largura):
            for y in range(altura):
                cor = self.imagem.get_at((x, y))[:3]  # Vai buscar a cor RGB do pixel
                if cor in self.cores_fundo:
                    self.imagem.set_at((x, y), (0, 0, 0, 0))  # Define o pixel como transparente

    def atualizar(self):
        # Atualiza a posição com base no sentido
        if self.sentido == "direita":
            self.x += self.velocidade
        elif self.sentido == "esquerda":
            self.x -= self.velocidade

    def desenhar(self, superficie):
        # Desenha o projétil na tela
        superficie.blit(self.imagem, (self.x, self.y))

    def saiu_do_ecra(self):
        # Verifica se o projétil saiu do ecrã (considerando ambos os sentidos)
        if self.sentido == "direita":
            return self.x > largura_ecra
        elif self.sentido == "esquerda":
            return self.x < 0

#em desenvolvimento, nao implementado, testar em main_tiago
class Projetil2:
    def __init__(self, x, y, duracao=4, velocidade=6):
        self.x = x
        self.y = y
        self.raio_fim_x = x + 64  # Exemplo de como definir raio_fim_x
        self.duracao = duracao  # Duração em segundos
        self.velocidade = velocidade
        self.sprites = self.carregar_sprites()
        self.tempo_decorrido = 0
        self.ativo = True
        #self.indice_sprite = 0
        self.estado_tecla = False  # Estado da tecla X
        self.tempo_por_frame = duracao / len(self.sprites)
        self.sprite_inicio = self.sprites[0]  # Parte inicial do raio
        self.sprite_corpo = self.sprites[1]  # Parte repetível do raio
        self.sprite_fim = self.sprites[2]  # Parte final do raio

    def carregar_sprites(self):
        # Adapta caminhos conforme os ficheiros do raio (início, corpo, fim)
        cor_fundo = (144, 176, 216) 
        caminhos = [
            "imagens/goku/projectil2/raio_inicio.gif",  # Parte inicial do raio
            "imagens/goku/projectil2/raio_corpo.gif",   # Parte repetível do raio
            "imagens/goku/projectil2/raio_fim.gif"      # Parte final do raio
        ]
        
        sprites = []
        for caminho in caminhos:
            sprite = pygame.image.load(caminho).convert()  # Carrega com fundo opaco
            sprite.set_colorkey(cor_fundo)  # Define a cor a ser tratada como transparente
            sprites.append(sprite)
        return sprites
    
    def atualizar(self, delta_tempo):
        if not self.ativo:
            return

        self.tempo_decorrido += delta_tempo

        # Continua o movimento até sair do ecrã
        self.x += self.velocidade

        # Desativa o raio apenas se sair do ecrã completamente
        if self.saiu_do_ecra():
            self.ativo = False
            self.tempo_decorrido = 0  # Reinicia o tempo decorrido para permitir uso futuro


    def desenhar(self, superficie):
        if not self.ativo:
            return

        # Calcula o comprimento total disponível para o raio
        comprimento_total = largura_ecra + 100
        largura_inicio = self.sprite_inicio.get_width()
        largura_fim = self.sprite_fim.get_width()
        largura_corpo = self.sprite_corpo.get_width()

        # Desenha o início do raio
        superficie.blit(self.sprite_inicio, (self.x, self.y))

        # Calcula o número de repetições necessárias para preencher o corpo
        comprimento_restante = comprimento_total - largura_inicio - largura_fim
        numero_repeticoes = max(0, comprimento_restante // largura_corpo)

        # Desenha o corpo do raio repetido
        for i in range(numero_repeticoes):
            pos_x = self.x + largura_inicio + i * largura_corpo
            superficie.blit(self.sprite_corpo, (pos_x, self.y))

        # Desenha o fim do raio
        pos_fim = self.x + largura_inicio + numero_repeticoes * largura_corpo
        superficie.blit(self.sprite_fim, (pos_fim, self.y))

    def saiu_do_ecra(self):
        # Verifica se a parte final do projétil saiu do ecrã
        return self.x > largura_ecra
    
    def verificar_colisao(self, alvo):
        raio_colisao = pygame.Rect(self.x, self.y, largura_ecra, 32)  # Define o raio do Projetil2
        alvo_colisao = pygame.Rect(alvo.x, alvo.y, alvo.largura, alvo.altura)  # Define o retângulo do inimgo
        return raio_colisao.colliderect(alvo_colisao)