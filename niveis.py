import pygame
import random
from inimigos import Inimigo
from config import largura_ecra, altura_ecra
from fadeinout import fade_in_out

# Função para carregar o fundo de acordo com o nível
def carregar_fundo(nivel):
    if nivel == 1:
        fundo = pygame.image.load("images/bg3.png").convert_alpha()  # Fundo do nível 1
    elif nivel == 2:
        fundo = pygame.image.load("images/bg2.png").convert_alpha()  # Fundo do nível 2
    elif nivel == 3:
        fundo = pygame.image.load("images/bg.png").convert_alpha()  # Fundo do nível 3
    else:
        fundo = pygame.image.load("images/bg.png").convert_alpha()  # Fundo padrão

    # Redimensiona o fundo para o tamanho da tela
    return pygame.transform.scale(fundo, (largura_ecra, altura_ecra))


def gerar_inimigo(nivel):
    if nivel == 1:
        tipo = random.choice([1, 2])  # Apenas inimigos do tipo 1 e 2 no nível 1
    elif nivel == 2:
        tipo = random.choice([2, 3])  # Apenas inimigos do tipo 2 e 3 no nível 2
    elif nivel == 3:
        tipo = 3  # Apenas inimigos do tipo 3 no nível 3
    else:
        tipo = random.choice([1, 2, 3])  # Para níveis superiores, inclui todos os tipos
    
    pos_y = random.randint(50, altura_ecra - 50)  # Posição vertical aleatória
    return Inimigo(tipo, pos_y)


def mostrar_historia(ecra, nivel):
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
    # Carregar a imagem da história baseada no nível
    if nivel == 1:
        imagem_historia = pygame.image.load("images/try4.jpg").convert_alpha()
        texto_historia = "Você é o herói que precisa salvar o universo!"
    elif nivel == 2:
        imagem_historia = pygame.image.load("images/bg2.png").convert_alpha()
        texto_historia = "Avançando para um novo desafio... Prepare-se!"
    elif nivel == 3:
        imagem_historia = pygame.image.load("images/bg3.png").convert_alpha()
        texto_historia = "O confronto final se aproxima!" 
    
    
    imagem_historia = pygame.transform.scale(imagem_historia, (largura_ecra, altura_ecra))  # Ajusta a imagem ao tamanho da tela

    # Desenha a imagem de fundo
    ecra.blit(imagem_historia, (0, 0))

    # Exibe o texto da história
    fonte = pygame.font.Font(None, 48)
    texto = fonte.render(texto_historia, True, (255, 255, 255))  # Texto em branco
    ecra.blit(texto, (largura_ecra // 2 - texto.get_width() // 2, altura_ecra // 3))

    # Desenha o botão "Continuar"
    fonte_botao = pygame.font.Font(None, 36)
    texto_botao = fonte_botao.render("Continuar", True, (255, 0, 0))  # Texto do botão em vermelho
    botao_rect = pygame.Rect(largura_ecra // 2 - texto_botao.get_width() // 2, altura_ecra // 2 + 100, texto_botao.get_width(), texto_botao.get_height())
    
    pygame.draw.rect(ecra, (0, 0, 0), botao_rect)  # Fundo do botão (preto)
    ecra.blit(texto_botao, (largura_ecra // 2 - texto_botao.get_width() // 2, altura_ecra // 2 + 100))  # Texto do botão

    pygame.display.update()  # Atualiza a tela

    # Espera até que o jogador clique no botão "Continuar"
    continuar = False
    while not continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):  # Verifica se o clique foi dentro do botão
                    continuar = True  # Quando o jogador clica, a história termina e o jogo continua

    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)


def mostrar_tela_final(ecra):
    
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
    # Define o fundo da tela final
    fundo_final = pygame.image.load("images/try2.jpg").convert_alpha()  # Imagem de fundo final
    fundo_final = pygame.transform.scale(fundo_final, (largura_ecra, altura_ecra))
    ecra.blit(fundo_final, (0, 0))

    # Exibe o texto "Jogo Completo"
    fonte_titulo = pygame.font.Font(None, 64)
    titulo = fonte_titulo.render("Jogo Completo!", True, (255, 255, 0))  # Texto amarelo
    ecra.blit(titulo, (largura_ecra // 2 - titulo.get_width() // 2, altura_ecra // 3))

    # Exibe os créditos
    fonte_creditos = pygame.font.Font(None, 36)
    creditos = [
        "Obrigado por jogar!",
        "Criado por: Tiago Bastos, Luis Oliveira, Carina Gameiro, Aleff Almeida e Guilherme Borges",
        "Desenvolvido em Python com Pygame"
    ]
    for i, linha in enumerate(creditos):
        texto_creditos = fonte_creditos.render(linha, True, (255, 255, 0))  # Texto amarelo
        ecra.blit(texto_creditos, (largura_ecra // 2 - texto_creditos.get_width() // 2, altura_ecra // 2 + i * 40))

    # Atualiza a tela e espera alguns segundos
    pygame.display.update()
    pygame.time.wait(10000)  # Aguarda 5 segundos antes de voltar ao menu
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)






