# jogador.py
import pygame
from projetil import Projetil

class Jogador:
    def __init__(self, pos_x, pos_y):
        # Posição inicial do jogador
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.animacoes = {}  # Dicionário para armazenar animações
        self.animacao_atual = None  # Animação que o jogador está a usar no momento
        self.projeteis = []  # Lista de projéteis disparados pelo jogador
        

    def adicionar_animacao(self, nome, animacao):
        # Adiciona uma animação ao dicionário de animações
        self.animacoes[nome] = animacao

    def definir_animacao(self, nome):
        # Define a animação atual para o jogador
        if nome in self.animacoes:
            self.animacao_atual = self.animacoes[nome]
            self.animacao_atual.reiniciar()  # Reinicia a animação para o início

    def atualizar(self, delta_tempo):
        # Atualiza a animação atual e projéteis
        if self.animacao_atual:
            self.animacao_atual.atualizar(delta_tempo)
        for projetil in self.projeteis:
            projetil.atualizar()  # Atualiza a posição dos projéteis
            if projetil.saiu_do_ecra():
                self.projeteis.remove(projetil)  # Remove projéteis fora da tela

    def desenhar(self, superficie):
        # Desenha o jogador e os projéteis na tela
        if self.animacao_atual:
            sprite = self.animacao_atual.obter_sprite_atual()
            superficie.blit(sprite, (self.pos_x, self.pos_y))
        for projetil in self.projeteis:
            projetil.desenhar(superficie)

    def disparar(self):
        # Cria um novo projetil e define a animação de disparo
        novo_projetil = Projetil(self.pos_x + 64, self.pos_y + 20)
        self.projeteis.append(novo_projetil)
        self.definir_animacao("disparar")

    def perder_vida(self, dano):
        # Diminui a vida do jogador ao ser atingido
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            print("Jogador morreu!")  # Mensagem de morte para debugging
            return False  # Indica que o jogador está morto
        return True  # Indica que o jogador ainda está vivo
