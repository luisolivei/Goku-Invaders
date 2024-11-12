import pygame
import os
#from menu import menu  # Importa o menu do arquivo menu.py

# Configuração inicial da janela e velocidade
largura_ecra = 800
altura_ecra = 600
velocidade_animacao = 0.03  # Velocidade de troca de frames de animação
velocidade_fundo = 0.8  # Velocidade de movimento do fundo

pygame.init()

# Classe do jogador
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

# Classe de animação base para carregar e controlar animações
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

# Subclasses para diferentes animações específicas do jogador
class AnimacaoParado(Personagem):
    def __init__(self):
        # Carrega os sprites da animação de estar parado
        caminhos_sprites = [
            "images/goku/parado/parado_1.gif",
        ]
        super().__init__(caminhos_sprites)

class AnimacaoAndar(Personagem):
    def __init__(self):
        # Carrega os sprites da animação de andar, esta a repetir a parada
        caminhos_sprites = [
            "images/goku/parado/parado_1.gif",
        ]
        super().__init__(caminhos_sprites)

class AnimacaoDisparar(Personagem):
    def __init__(self):
        # Carrega os sprites da animação de disparar
        caminhos_sprites = [
            "images/goku/disparar/disparar_1.gif", "images/goku/disparar/disparar_2.gif","images/goku/disparar/disparar_3.gif","images/goku/disparar/disparar_4.gif","images/goku/disparar/disparar_5.gif",
        ]
        super().__init__(caminhos_sprites)

class AnimacaoAtingido(Personagem):
    def __init__(self):
        # Carrega os sprites da animação de estar atingido
        caminhos_sprites = [
            "images/goku/disparar/disparar_1.gif",
        #    "images/goku/atingido/frame1.png", "images/goku/atingido/frame2.png",
        ]
        super().__init__(caminhos_sprites)

# Classe para projéteis disparados pelo jogador
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

# Função para o menu inicial
def menu():
    # Define o texto e a posição para o botão "Play"
    font = pygame.font.Font(None, 74)
    play_text = font.render("Play", True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(largura_ecra // 2, altura_ecra // 2))
    
    # Loop principal do menu
    while True:
        ecra.blit(fundo, (0, 0))  # Exibe o fundo do menu
        ecra.blit(play_text, play_rect)  # Exibe o texto "Play" no centro da tela

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(evento.pos):
                    return True  # Inicia o jogo se "Play" for clicado

        pygame.display.update()

# Função principal do jogo
def play():
    pygame.display.set_caption("Goku Invaders")
    # Inicializa o jogador e define animações
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2)
    jogador.adicionar_animacao("parado", AnimacaoParado())
    jogador.adicionar_animacao("andar", AnimacaoAndar())
    jogador.adicionar_animacao("disparar", AnimacaoDisparar())
    jogador.adicionar_animacao("atingido", AnimacaoAtingido())
    jogador.definir_animacao("parado") #necessaria para iniciar
    
    a_funcionar = True
    relogio = pygame.time.Clock()
    posicao_fundo_x = 0 # Posição inicial do fundo

    # Loop principal do jogo
    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Calcula o tempo entre frames

        # Processa eventos de entrada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.disparar()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    jogador.definir_animacao("parado")  # Retorna à animação "parado" ao soltar a tecla

        # Verifica as teclas pressionadas para movimento vertical
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and jogador.pos_y > 0:
            jogador.pos_y -= 5
            jogador.definir_animacao("andar")
        elif tecla[pygame.K_DOWN] and jogador.pos_y < altura_ecra - 64:
            jogador.pos_y += 5
            jogador.definir_animacao("andar")
#        else:
#            jogador.definir_animacao("parado")  # Muda para "parado" se não estiver a mover

        # Atualiza a posição do fundo para movimento contínuo
        posicao_fundo_x -= velocidade_fundo
        if posicao_fundo_x <= -largura_ecra:
            posicao_fundo_x = 0

        # Desenha o fundo em movimento e o jogador
        ecra.blit(fundo, (posicao_fundo_x, 0))
        ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))

        # Atualizar e desenhar o jogadortempo)
        jogador.desenhar(ecra)

        pygame.display.update()

def mostrar_score():
    print("Exibindo pontuação...")
    pygame.time.wait(2000) 


# Configuração do fundo e execução do menu
ecra = pygame.display.set_mode((largura_ecra, altura_ecra))
pygame.display.set_caption("Menu")
fundo = pygame.image.load("images/bg.png").convert_alpha()
fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

# Loop principal para exibir o menu e reagir à seleção do jogador
while True:
    escolha = menu(ecra, largura_ecra, altura_ecra, fundo)  # Chamada correta da função menu
    if escolha == "play":
        play()  # Chama a função play para iniciar o jogo
    elif escolha == "score":
        mostrar_score()  # Chama a função mostrar_score para exibir a pontuação
    elif escolha == "quit":
        break  # Sai do loop e fecha o jogo

pygame.quit()
