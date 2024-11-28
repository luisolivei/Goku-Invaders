# projetil.py
import pygame
from config import largura_ecra

class Projetil:
    def __init__(self, x, y, velocidade=5, cores_fundo=[(144, 176, 216)]):
        # Inicializa a posição e velocidade do projetil
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.imagem = pygame.image.load("images/chama_disparos.gif").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (20, 20))  # Ajusta o tamanho da imagem
        self.cores_fundo = cores_fundo
        self.remover_cores_fundo()
    
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
        # Move o projetil horizontalmente
        self.x += self.velocidade

    def desenhar(self, superficie):
        # Desenha o projétil na tela
        superficie.blit(self.imagem, (self.x, self.y))

    def saiu_do_ecra(self):
        # Verifica se o projetil saiu da tela
        return self.x > largura_ecra
