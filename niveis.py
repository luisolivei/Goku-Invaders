import pygame
import cv2
import numpy as np
import random
from inimigos import Inimigo
from config import largura_ecra, altura_ecra, caminho_fonte
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


def reproduzir_video(video_path, ecra):
    # Carrega o vídeo com OpenCV
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Erro ao abrir o vídeo!")
        return

    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        ret, frame = cap.read()
        if not ret:
            break  # Se o vídeo terminar, sai do loop

        # Redimensiona o quadro do vídeo para caber na janela do jogo
        frame = cv2.resize(frame, (largura_ecra, altura_ecra))

        # Converte o quadro para o formato adequado para o Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.transpose(frame, (1, 0, 2))
        frame = np.flip(frame, axis=0)
        frame = pygame.surfarray.make_surface(frame)

        ecra.blit(frame, (0, 0))
        pygame.display.update()
        pygame.time.wait(95)
        clock.tick(60)  # Limita a 30 FPS para uma reprodução suave

    cap.release()


def mostrar_historia(ecra, nivel):
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)
    
    # Carregar a imagem da história baseada no nível
    if nivel == 1:
        imagem_historia = pygame.image.load("images/historia1.png").convert_alpha()
        texto_historia = "Raptamos a Kika!!! Conseguiras resgata-la?"
    elif nivel == 2:
        imagem_historia = pygame.image.load("images/historia1.png").convert_alpha()
        texto_historia = "Raptamos a Kika!!! Conseguiras resgata-la?"
    elif nivel == 3:
        imagem_historia = pygame.image.load("images/historia2.jpg").convert_alpha()
        texto_historia = "Percorri o universo e nao a encontrei!! Sera Agora?"  
    elif nivel > 3:  # História final
        reproduzir_video("tryf.mp4", ecra)
        return

    imagem_historia = pygame.transform.scale(imagem_historia, (largura_ecra, altura_ecra))  # Ajusta a imagem ao tamanho da tela

    # Desenha a imagem de fundo
    ecra.blit(imagem_historia, (0, 0))

    # Exibe o texto da história
    fonte = pygame.font.Font(None, 46)

    # Fundo opaco para o texto da história
    texto_surface = fonte.render(texto_historia, True, (255, 255, 255))  # Texto em branco
    texto_fundo = pygame.Surface((texto_surface.get_width(), texto_surface.get_height()))
    texto_fundo.fill((0, 0, 0))  # Fundo preto
    texto_fundo.set_alpha(200)  # Reduz opacidade do fundo para 200

    # Posiciona fundo e texto
    texto_x = largura_ecra // 2 - texto_surface.get_width() // 2
    texto_y = altura_ecra // 2 + 200
    ecra.blit(texto_fundo, (texto_x, texto_y))  # Fundo do texto
    ecra.blit(texto_surface, (texto_x, texto_y))  # Texto em si

    # Desenha o botão "Continuar" no canto inferior direito
    fonte_botao = pygame.font.Font(None, 38)
    texto_botao = fonte_botao.render("Continuar", True, (255, 0, 0))  # Texto do botão em vermelho

    # Fundo opaco do botão
    botao_surface = pygame.Surface((texto_botao.get_width() + 20, texto_botao.get_height() + 10))  # Margem ao redor do texto
    botao_surface.fill((0, 0, 0))  # Fundo preto
    botao_surface.set_alpha(200)  # Reduz opacidade do fundo do botão

    # Posiciona o botão
    botao_x = largura_ecra - texto_botao.get_width() - 40  # 20 px de margem direita + margem extra do fundo
    botao_y = altura_ecra - texto_botao.get_height() - 30  # 20 px de margem inferior + margem extra do fundo
    botao_rect = pygame.Rect(botao_x, botao_y, texto_botao.get_width() + 20, texto_botao.get_height() + 10)  # Define o retângulo

    ecra.blit(botao_surface, (botao_x, botao_y))  # Fundo opaco do botão
    ecra.blit(texto_botao, (botao_x + 10, botao_y + 5))  # Texto centralizado no fundo do botão

    pygame.display.update()  # Atualiza a tela
    
    # Espera até que o jogador pressione Enter ou clique no botão "Continuar"
    continuar = False
    while not continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Verifica se o mouse foi clicado no botão
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):  # Verifica se o clique foi dentro do botão
                    continuar = True
        # Verifica se a tecla Enter foi pressionada
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Tecla Enter
                    continuar = True
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)

def mostrar_tela_final(ecra,):
    
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)


    # Define o fundo da tela final
    fundo_final = pygame.image.load("images/try2.jpg").convert_alpha()  # Imagem de fundo final
    fundo_final = pygame.transform.scale(fundo_final, (largura_ecra, altura_ecra))  # Redimensiona suavemente
    ecra.blit(fundo_final, (0, 0))

    # Exibe o texto "Jogo Completo"
    fonte_titulo = pygame.font.Font(caminho_fonte, 64)
    titulo = fonte_titulo.render("Resgataste a Kika", True, (0, 0, 0))  # Texto amarelo
    ecra.blit(titulo, (largura_ecra // 2 - titulo.get_width()  // 2, altura_ecra // 3-100))

    # Exibe os créditos
    fonte_creditos = pygame.font.Font(caminho_fonte, 40)
    creditos = [
        "Obrigado por jogar!",
        "Jogo Criado por:",
        "Tiago Bastos",
        "Luis Oliveira ",
        "Carina Gameiro", 
        "Aleff Almeida",
        "Guilherme Borges",
        
    ]
    for i, linha in enumerate(creditos):
        texto_creditos = fonte_creditos.render(linha, True, (255, 255, 0, 200) )  # Texto amarelo
        ecra.blit(texto_creditos, (largura_ecra // 2 - texto_creditos.get_width() // 2, altura_ecra // 2 + i * 40))

    # Atualiza a tela e espera alguns segundos
    pygame.display.update()
    pygame.time.wait(10000)  # Aguarda 5 segundos antes de voltar ao menu
    fade_in_out(ecra, (0, 0, 0), largura_ecra, altura_ecra, 20)

def nivel_concluido(ecra, nivel):
    fonte = pygame.font.Font(caminho_fonte, 64)
    mensagem = f"Nível {nivel} concluído!"
    texto = fonte.render(mensagem, True, (255, 255, 0))  # Amarelo
    ecra.blit(texto, (largura_ecra // 2 - texto.get_width() // 2, altura_ecra // 2))
    pygame.display.update()
    pygame.time.wait(2000)