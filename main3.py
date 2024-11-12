import pygame
from menu import menu  # Importa o menu do arquivo menu.py

# Configuração inicial
largura_ecra = 800
altura_ecra = 600
velocidade_animacao = 0.1
velocidade_fundo = 0.8  
caminho_sprite_sheet = "images/goku/parado/parado_1.gif"

pygame.init()
ecra = pygame.display.set_mode((largura_ecra, altura_ecra))
pygame.display.set_caption("Menu")

# Classe do jogador
class Jogador:
    def __init__(self, pos_x, pos_y, sprite_sheet):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite_sheet = sprite_sheet
        self.animacoes = {}
        self.animacao_atual = None
        self.projeteis = []

    def adicionar_animacao(self, nome, animacao):
        self.animacoes[nome] = animacao

    def definir_animacao(self, nome):
        if nome in self.animacoes:
            self.animacao_atual = self.animacoes[nome]
            self.animacao_atual.reiniciar()

    def atualizar(self, delta_tempo):
        if self.animacao_atual:
            self.animacao_atual.atualizar(delta_tempo)
        for projetil in self.projeteis:
            projetil.atualizar()
            if projetil.saiu_do_ecra():
                self.projeteis.remove(projetil)

    def desenhar(self, superficie):
        if self.animacao_atual:
            sprite = self.animacao_atual.obter_sprite_atual()
            superficie.blit(sprite, (self.pos_x, self.pos_y))
        for projetil in self.projeteis:
            projetil.desenhar(superficie)

    def disparar(self):
        novo_projetil = Projetil(self.pos_x + 64, self.pos_y + 20)  # Posição de saída do projétil
        self.projeteis.append(novo_projetil)

# Classe de animação
class Personagem:
    def __init__(self, sprite_sheet, dados_sprite, cor_chave=(160, 192, 192)): #cor rgb a filtrar as imagens
        self.sprite_sheet = sprite_sheet
        self.dados_sprite = dados_sprite
        self.sprites = []
        self.indice_sprite = 0
        self.tempo_desde_ultimo_sprite = 0
        self.cor_chave = cor_chave
        self.carregar_sprites()

    def carregar_sprites(self):
        for dados in self.dados_sprite:
            x, y, largura, altura = dados
            sprite = self.sprite_sheet.subsurface(pygame.Rect(x, y, largura, altura))
            sprite.set_colorkey(self.cor_chave)
            self.sprites.append(sprite)

    def reiniciar(self):
        self.indice_sprite = 0
        self.tempo_desde_ultimo_sprite = 0

    def atualizar(self, delta_tempo):
        self.tempo_desde_ultimo_sprite += delta_tempo
        if self.tempo_desde_ultimo_sprite >= velocidade_animacao:
            self.indice_sprite = (self.indice_sprite + 1) % len(self.sprites)
            self.tempo_desde_ultimo_sprite = 0

    def obter_sprite_atual(self):
        return self.sprites[self.indice_sprite]

# Subclasse para animação de disparo
class AnimacaoPersonagem(Personagem):
    def __init__(self, sprite_sheet):
        dados_sprite = [
            (0, 0, 64, 80), (64, 0, 40, 80), (100, 0, 64, 80), (110+64, 0, 64, 80), (220, 0, 63, 80),
        ]
        super().__init__(sprite_sheet, dados_sprite)

# Classe para projéteis
class Projetil:
    def __init__(self, x, y, velocidade=5):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.largura = 10
        self.altura = 10
        self.cor = (255, 255, 0)  # Cor amarela para o projétil

    def atualizar(self):
        self.x += self.velocidade

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, (self.x, self.y, self.largura, self.altura))

    def saiu_do_ecra(self):
        return self.x > largura_ecra

# Função principal do jogo
def play():
    pygame.display.set_caption("Goku Invaders")
    jogador = Jogador(100, altura_ecra / 2 - 64 / 2, sprite_sheet)
    jogador.adicionar_animacao("disparo",AnimacaoPersonagem(sprite_sheet))
    jogador.definir_animacao("disparo")  # Animação inicial
    
    a_funcionar = True
    relogio = pygame.time.Clock()
    posicao_fundo_x = 0  # Posição inicial do fundo

    while a_funcionar:
        delta_tempo = relogio.tick(60) / 1000  # Tempo entre frames

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_funcionar = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.disparar()

        # Movimento com as setas para cima e para baixo
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and jogador.pos_y > 0:
            jogador.pos_y -= 5
        if tecla[pygame.K_DOWN] and jogador.pos_y < altura_ecra - 64:
            jogador.pos_y += 5

        # Atualizar posição do fundo para movimento contínuo
        posicao_fundo_x -= velocidade_fundo
        if posicao_fundo_x <= -largura_ecra:
            posicao_fundo_x = 0

        # Desenhar fundo com rolagem
        ecra.blit(fundo, (posicao_fundo_x, 0))
        ecra.blit(fundo, (posicao_fundo_x + largura_ecra, 0))

        # Atualizar e desenhar o jogador
        jogador.atualizar(delta_tempo)
        jogador.desenhar(ecra)

        pygame.display.update()

def mostrar_score():
    print("Exibindo pontuação...")
    pygame.time.wait(2000) 

# Carregar imagens e configurar fundo e jogador
sprite_sheet = pygame.image.load(caminho_sprite_sheet).convert()
sprite_sheet.set_colorkey((144, 176, 216))  # Define filtro para tornar fundo transparente
fundo = pygame.image.load("images/bg.png").convert_alpha()
fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

# Loop principal para exibir o menu e reagir à seleção do jogador
while True:
    escolha = menu(ecra, largura_ecra, altura_ecra, fundo)
    if escolha == "play":
        play()
    elif escolha == "score":
        mostrar_score()
    elif escolha == "quit":
        break

pygame.quit()
