# projetil.py
import pygame
from config import largura_ecra

class Projetil:
    def __init__(self, x, y, velocidade=5):
        # Inicializa a posição e velocidade do projetil
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.largura = 10
        self.altura = 10
        self.cor = (255, 255, 0)  # Cor amarela para o projétil

    def atualizar(self):
        # Move o projetil horizontalmente
        self.x += self.velocidade

    def desenhar(self, superficie):
        # Desenha o projétil na tela
        pygame.draw.rect(superficie, self.cor, (self.x, self.y, self.largura, self.altura))

    def saiu_do_ecra(self):
        # Verifica se o projetil saiu da tela
        return self.x > largura_ecra
