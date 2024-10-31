import pygame

# Configuração inicial
largura_ecra = 800
altura_ecra = 600
velocidade_animacao = 0.1  # Velocidade de transição dos sprites
caminho_sprite_sheet = "images/14491.gif"

pygame.init()
ecra = pygame.display.set_mode((largura_ecra, altura_ecra))
pygame.display.set_caption("Goku-Invaders")

# Classe básica do jogador
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
        novo_projetil = Projetil(self.pos_x + 64, self.pos_y + 32)  # Posição inicial do projétil
        self.projeteis.append(novo_projetil)

# Classe base de animação
class Animacao:
    def __init__(self, sprite_sheet, dados_sprite, cor_chave=(144, 176, 216)):
        self.sprite_sheet = sprite_sheet
        self.dados_sprite = dados_sprite  # Lista de tuplas com (x, y, largura, altura)
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

# Subclasse para animação de disparo de projéteis
class AnimacaoDisparo(Animacao):
    def __init__(self, sprite_sheet):
        dados_sprite = [
            (0, 2304, 64, 64), (64, 2304, 70, 64), (136, 2304, 70, 64),
            (136+64, 2304, 70, 64), (136+128, 2304, 70, 64)
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
        self.x += self.velocidade  # Movimento horizontal para a direita

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, (self.x, self.y, self.largura, self.altura))

    def saiu_do_ecra(self):
        return self.x > largura_ecra  # Se o projétil saiu do limite da tela

# Carregar imagens e configurar jogador
sprite_sheet = pygame.image.load(caminho_sprite_sheet).convert()
sprite_sheet.set_colorkey((144, 176, 216))  # Define o azul como transparente

# Carregar e dimensionar o fundo
fundo = pygame.image.load("images/bg.png").convert_alpha()
fundo = pygame.transform.scale(fundo, (largura_ecra, altura_ecra))

# Configurar o jogador e sua animação de tiro
jogador = Jogador(100, altura_ecra / 2 - 64 / 2, sprite_sheet)
jogador.adicionar_animacao("disparo", AnimacaoDisparo(sprite_sheet))
jogador.definir_animacao("disparo")  # Animação inicial

# Loop principal
a_funcionar = True
relogio = pygame.time.Clock()

while a_funcionar:
    delta_tempo = relogio.tick(60) / 1000  # Tempo entre frames

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            a_funcionar = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jogador.disparar()

    # Atualizar e desenhar
    ecra.blit(fundo, (0, 0))
    jogador.atualizar(delta_tempo)
    jogador.desenhar(ecra)

    pygame.display.update()

pygame.quit()
