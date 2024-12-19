import pygame
import os
from config import largura_ecra, altura_ecra, caminho_fonte
def mostrar_highscore(ecra, fundo):
    # Configuração do fundo
    ecra.blit(fundo, (0, 0))
    
    try:
        # Lê o arquivo de highscore
        with open(arquivo_score, "r") as arquivo:
            highscore = arquivo.read().strip()
    except IOError:
        highscore = "Nenhum highscore salvo."
    
    # Configuração do texto
    fonte = pygame.font.Font(caminho_fonte, 48)
    titulo = fonte.render("Pontuação mais alta", True, (255, 255, 0))
    texto_highscore = fonte.render(highscore, True, (255, 255, 0))
    instrucoes = fonte.render("Pressione ESC para voltar", True, (200, 200, 200))
    
    # Centraliza o texto na tela
    ecra.blit(titulo, (largura_ecra // 2 - titulo.get_width() // 2, altura_ecra // 4))
    ecra.blit(texto_highscore, (largura_ecra // 2 - texto_highscore.get_width() // 2, altura_ecra // 2-80))
    ecra.blit(instrucoes, (largura_ecra // 2 - instrucoes.get_width() // 2, altura_ecra - 100))
    
    #pygame.display.update()
    
    # Aguarda o jogador pressionar ESC para voltar ao menu
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
        pygame.display.update()


# Caminho para salvar o arquivo de score
arquivo_score = "highscore.txt"

def salvar_highscore(score):
    try:
        with open(arquivo_score, "w") as arquivo:
            arquivo.write(str(score))
    except IOError:
        print("Erro ao salvar o highscore.")

def carregar_highscore():
    if os.path.exists(arquivo_score):
        try:
            with open(arquivo_score, "r") as arquivo:
                return int(arquivo.read().strip())
        except (IOError, ValueError):
            return 0  # Se houver erro, retorna 0
    return 0  # Se o arquivo não existir, retorna 0