import pygame
from config import largura_ecra

class Inimigo:
    def __init__(self, tipo, pos_y, escala=50, cores_fundo=[(132, 66, 4)]):
        # Inicializa o inimigo com base no tipo e define os atributos
        self.tipo = tipo  # Tipo do inimigo (1, 2 ou 3)
        self.vidas = {1: 3, 2: 5, 3: 7}[tipo]  # Define o número de vidas conforme o tipo
        self.pos_x = largura_ecra  # Aparece da direita do ecrã
        self.pos_y = pos_y  # Posição vertical especificada
        self.velocidade = 1  # Velocidade do inimigo (podes ajustar conforme necessário)
        self.escala = escala / 100  # Fator de escala, padrão 100% (sem redimensionamento)
        self.cores_fundo = cores_fundo  # Lista de cores de fundo a serem removidas

        # Define as animações para cada estado do inimigo
        self.animacoes = {
            "andar": self.carregar_sprites("andar"),  # Animação de movimento
            #"atingido": self.carregar_sprites("atingido"), #trocar por atingido quando tiver imagens disponiveis
            "morto": self.carregar_sprites("morto")
        }
        self.animacao_atual = "andar"  # Começa com a animação de andar
        self.indice_sprite = 0  # Índice do sprite atual
        self.tempo_desde_ultimo_sprite = 0
        self.velocidade_animacao = 0.1  # Velocidade de troca de frames da animação

        self.vivo = True  # Define se o inimigo está ativo no ecrã

    def carregar_sprites(self, estado):
        # Carrega os sprites para um estado específico do inimigo (andar, atingido, ou morto)
        sprites = []
        for i in range(1, 4):  # Supondo que temos 3 frames de animação por estado
            caminho = f"images/Inimigos/inimigo_{self.tipo}/inimigo_{self.tipo}_{estado}_{i}.gif"
            sprite = pygame.image.load(caminho).convert_alpha()

            # Remove as cores de fundo especificadas
            sprite = self.remover_cores_fundo(sprite)

            # Inverte a imagem horizontalmente para que o inimigo fique voltado para a esquerda
            sprite = pygame.transform.flip(sprite, True, False)
            
            # Redimensiona o sprite
            sprite = self.redimensionar_sprite(sprite)

            sprites.append(sprite)
        return sprites

    def remover_cores_fundo(self, sprite):
        # Remove várias cores de fundo da imagem, tornando-as transparentes
        for x in range(sprite.get_width()):
            for y in range(sprite.get_height()):
                cor = sprite.get_at((x, y))  # Obtém a cor do pixel na posição (x, y)
                if cor[0:3] in self.cores_fundo:  # Se a cor do pixel estiver na lista de cores de fundo
                    sprite.set_at((x, y), (0, 0, 0, 0))  # Torna o pixel transparente
        return sprite

    def redimensionar_sprite(self, sprite):
        # Redimensiona o sprite com base no fator de escala
        largura_original, altura_original = sprite.get_size()
        nova_largura = int(largura_original * self.escala)
        nova_altura = int(altura_original * self.escala)
        return pygame.transform.scale(sprite, (nova_largura, nova_altura))

    def atualizar(self, delta_tempo, jogador):
        # Atualiza a posição do inimigo e a animação
        if not self.vivo:
            return

        # Atualiza a animação do inimigo
        self.tempo_desde_ultimo_sprite += delta_tempo
        if self.tempo_desde_ultimo_sprite >= self.velocidade_animacao:
            self.indice_sprite = (self.indice_sprite + 1) % len(self.animacoes[self.animacao_atual])
            self.tempo_desde_ultimo_sprite = 0

        # Move o inimigo para a esquerda em direção ao jogador
        self.pos_x -= self.velocidade

        # Atualiza a animação para "morto" se as vidas acabaram
        if self.vidas <= 0:
            self.animacao_atual = "morto"
            self.vivo = False  # Marca o inimigo como morto para ser removido

    def desenhar(self, ecra):
        # Desenha o inimigo no ecrã
        if self.vivo:
            sprite = self.animacoes[self.animacao_atual][self.indice_sprite]
            ecra.blit(sprite, (self.pos_x, self.pos_y))

    def verificar_colisao(self, projetil):
        # Verifica se há colisão entre o projétil e o inimigo
        if not self.vivo:
            return False

        # Obter retângulos de colisão do inimigo e do projétil
        sprite = self.animacoes[self.animacao_atual][self.indice_sprite]
        inimigo_rect = sprite.get_rect(topleft=(self.pos_x, self.pos_y))
        projetil_rect = pygame.Rect(projetil.x, projetil.y, projetil.largura, projetil.altura)

        # Se houver colisão, diminui a vida do inimigo e altera a animação
        if inimigo_rect.colliderect(projetil_rect):
            self.vidas -= 1  # Diminui uma vida
            #self.animacao_atual = "atingido"  # Define a animação de atingido temporariamente
            self.animacao_atual = "andar"

            # Retorna à animação de andar após ser atingido
            if self.vidas > 0:
                self.animacao_atual = "andar"

            return True  # Colisão ocorreu

        return False  # Sem colisão
